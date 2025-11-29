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

# Debug endpoint
@router.get("/documents")
async def list_documents():
    """List all available document IDs for debugging"""
    stored_ids = {}
    if hasattr(knowledge_repo.vector_store, 'metadata'):
        for item in knowledge_repo.vector_store.metadata:
            doc_id = item.get("doc_id") or item.get("document_id")
            if doc_id:
                stored_ids[doc_id] = {
                    "filename": item.get("filename", "unknown"),
                    "has_text": len(item.get("text", "")) > 0,
                    "text_length": len(item.get("text", ""))
                }
    return {"count": len(stored_ids), "documents": stored_ids}

# Instantiate AI Agents
classifier = DocumentClassifier()
# Use the shared vector store from knowledge_repo
finder = RegulationFinder(
    index_path=knowledge_repo.vector_store.index_file,
    store_path=knowledge_repo.vector_store.metadata_file
)
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
        # Try with a timeout
        import asyncio
        response = await asyncio.wait_for(
            chat.send_message_async(prompt_text),
            timeout=15.0  # 15 second timeout
        )
        return response.text
    except asyncio.TimeoutError:
        logger.error("Gemini API timed out after 15 seconds")
        # Fallback response when API times out
        return f"Based on the available context, here's an analysis of your query: '{query}'\n\n[Note: Using cached analysis due to API timeout. The system found {len(context_docs)} relevant documents but the AI service is currently slow. Please try again or contact support if this persists.]"
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Error generating response from Gemini: {e}\n{error_details}")
        # Fallback response with context
        context_summary = "\n".join([f"- {doc.get('text', '')[:100]}..." for doc in context_docs[:2]])
        return f"Analysis of: '{query}'\n\nRelevant context found:\n{context_summary}\n\n[Note: AI processing temporarily unavailable. Showing raw context instead.]"


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
    logger.info(f"Analyse request for file_id: {req.file_id}")
    
    if not req.file_id:
        raise HTTPException(status_code=400, detail="file_id is required for this endpoint")

    # Reload the vector store to pick up newly uploaded documents
    if hasattr(knowledge_repo.vector_store, 'load'):
        knowledge_repo.vector_store.load()
    
    # Also reload the regulation finder's vector store
    if hasattr(finder.vector_store, 'load'):
        finder.vector_store.load()
    
    text = knowledge_repo.get_document_text(req.file_id)
    
    # Debug logging
    if not text:
        # Check what documents are actually in the store
        if hasattr(knowledge_repo.vector_store, 'metadata'):
            stored_ids = set()
            for item in knowledge_repo.vector_store.metadata:
                doc_id = item.get("doc_id") or item.get("document_id")
                if doc_id:
                    stored_ids.add(doc_id)
            logger.error(f"Document text not found for ID: {req.file_id}. Available IDs in store: {stored_ids}")
        else:
            logger.error(f"Document text not found for ID: {req.file_id}. Vector store has no metadata.")
        
        raise HTTPException(status_code=404, detail=f"Document text not found for ID: {req.file_id}. The document may not have been fully processed.")
    
    logger.info(f"Successfully retrieved text for document {req.file_id}, length: {len(text)}")

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
