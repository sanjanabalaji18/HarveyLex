from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os

from datastore.knowledge_repository import KnowledgeRepository
from core.memory import memory_service

from core.logger import get_logger

from typing import Optional
from ai_modules.document_classifier import DocumentClassifier
from ai_modules.regulation_finder import RegulationFinder
from ai_modules.summary_agent import SummaryAgent

# Configure the Gemini API key
# Make sure to set the GOOGLE_API_KEY environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()
knowledge_repo = KnowledgeRepository()
logger = get_logger(__name__)

# Instantiate AI Agents
classifier = DocumentClassifier()
finder = RegulationFinder()
summary_agent = SummaryAgent()

# --- Pydantic Models ---
class AnalysisRequest(BaseModel):
    query: str
    session_id: str  # Added to track conversation
    file_id: Optional[str] = None

class AnalysisResponse(BaseModel):
    answer: str
    sources: list

# --- Helper Functions ---
async def generate_contextual_answer(query: str, history: list, context_docs: list):
    """Generates an answer using Gemini, with conversation history and context."""
    
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Build the prompt
    context_str = "\n\n".join([f"Source {i+1}: {doc['text']}" for i, doc in enumerate(context_docs)])
    
    # Format history for the model
    formatted_history = []
    for message in history:
        # Ensure role is either 'user' or 'model'
        role = message.get("role", "user")
        if role not in ["user", "model"]:
            role = "user" # Default to user if role is something else
        formatted_history.append({"role": role, "parts": [message.get("content", "")]})

    prompt_text = f"""
    You are HarveyLex, a professional legal compliance AI assistant.
    Based on the provided conversation history and the following context from legal documents, answer the user's query.
    Your answer must be concise, professional, and directly address the query.
    Cite the sources you used in your answer (e.g., [Source 1]).

    CONTEXT:
    {context_str}

    QUERY:
    {query}
    """
    
    # Create a chat session with history
    chat = model.start_chat(history=formatted_history)
    
    try:
        response = await chat.send_message_async(prompt_text)
        return response.text
    except Exception as e:
        logger.error(f"Error generating response from Gemini: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate AI response.")


# --- API Endpoints ---
@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_documents(request: AnalysisRequest):
    """
    Analyzes a user query against the knowledge base with conversational context.
    """
    logger.info(f"Received analysis request for session_id: {request.session_id}")
    
    # 1. Retrieve relevant documents from the knowledge base
    try:
        context_docs = await knowledge_repo.search(request.query, top_k=3)
        if not context_docs:
            logger.warning(f"No documents found for query: '{request.query}'")
    except Exception as e:
        logger.error(f"Error during knowledge base search: {e}")
        raise HTTPException(status_code=500, detail="Failed to search knowledge base.")

    # 2. Get conversation history from memory
    history = memory_service.get_history(request.session_id)
    logger.info(f"Retrieved {len(history)} messages from history for session {request.session_id}")

    # 3. Generate a contextual answer using the LLM
    answer = await generate_contextual_answer(request.query, history, context_docs)

    # 4. Update the conversation history
    memory_service.add_message(request.session_id, "user", request.query)
    memory_service.add_message(request.session_id, "model", answer)
    logger.info(f"Updated history for session {request.session_id}")

    return AnalysisResponse(
        answer=answer,
        sources=[{"doc_id": doc.get("doc_id", "unknown"), "text": doc.get("text", "")} for doc in context_docs]
    )

@router.post("/analyse")
async def analyse(req: AnalysisRequest):
    """
    Advanced analysis endpoint using document classification and regulation finding.
    """
    if not req.file_id:
        raise HTTPException(status_code=400, detail="file_id is required for this endpoint")

    text = knowledge_repo.get_document_text(req.file_id)
    if not text:
        # Try to find by partial ID match if exact match fails (sometimes IDs get truncated or modified)
        logger.warning(f"Document text not found for ID: {req.file_id}. Attempting fallback search.")
        # This is a simple fallback, in production we'd want more robust ID handling
        pass
        
    if not text:
        raise HTTPException(status_code=404, detail=f"Document text not found for ID: {req.file_id}")

    doc_type = classifier.classify_document(text)

    if "legal" in doc_type.lower():
        # Use the query from request to find regulations
        results = await finder.search(req.query, k=5)
        summary = summary_agent.summarize(text, results, query=req.query)
        return {
            "type": doc_type,
            "message": "Legal document detected. Compliance analysis:",
            "summary": summary,
            "regulations": results
        }
    else:
        # Even for non-legal docs, if there's a query, we should answer it
        if req.query:
             # Use the same summarizer but maybe with less strict legal context if needed
             # For now, we reuse the robust summarizer to answer the question
             results = await finder.search(req.query, k=3)
             summary = summary_agent.summarize(text, results, query=req.query)
             return {
                "type": "non-legal",
                "message": "Document analysis:",
                "summary": summary,
                "regulations": results
             }
        else:
            return {
                "type": "non-legal",
                "message": "This document does not appear to be legal. Here is a general summary:",
                "summary": summary_agent.basic_summary(text)
            }
