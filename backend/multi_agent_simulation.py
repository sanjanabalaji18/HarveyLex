from fastapi import FastAPI, APIRouter, UploadFile
import asyncio
import random
from typing import Dict, List, Optional
from pydantic import BaseModel
import uuid

# --- Shared Data Stores (In-Memory for demo) ---
document_store = {}
vector_store = {}

# --- Data Models ---
class AgentResponse(BaseModel):
    answer: str
    citations: List[int]
    confidence: float
    agent_trace: List[str]

class AnalysisRequest(BaseModel):
    query: str
    session_id: str

# --- AGENT CLASSES ---

class IngestionAgent:
    """Handles file parsing, OCR (simulated), and cleaning."""
    async def process(self, filename: str) -> Dict:
        print(f"[IngestionAgent] Reading {filename}...")
        await asyncio.sleep(1.5)  # Simulate OCR
        return {
            "status": "extracted",
            "raw_text": f"Simulated legal text content for {filename}..." * 50,
            "page_count": random.randint(5, 50),
            "filename": filename
        }

class VectorAgent:
    """Handles semantic chunking and embedding generation."""
    async def embed_and_store(self, doc_id: str, raw_text: str):
        print(f"[VectorAgent] Chunking and embedding {doc_id}...")
        await asyncio.sleep(1.0)
        
        # Simulate chunking
        chunks = [
            {"id": 1, "text": "Limitation of Liability: The total liability shall not exceed...", "page": 8},
            {"id": 2, "text": "Termination: Either party may terminate with 30 days notice.", "page": 12},
            {"id": 3, "text": "Governing Law: This agreement is governed by the laws of New York.", "page": 14},
            {"id": 4, "text": "Confidentiality: Receiving party must protect proprietary info.", "page": 3},
            {"id": 5, "text": "Data Protection: Processor agrees to comply with GDPR.", "page": 24},
        ]
        vector_store[doc_id] = chunks
        print(f"[VectorAgent] Stored {len(chunks)} vectors for {doc_id}")
        return len(chunks)

class AnalysisAgent:
    """Retrieves relevant chunks and applies legal reasoning."""
    async def analyze(self, doc_id: str, query: str) -> Dict:
        print(f"[AnalysisAgent] Reasoning on query: {query}")
        await asyncio.sleep(1.2)
        
        chunks = vector_store.get(doc_id, [])
        # Simple keyword retrieval simulation
        relevant_chunks = []
        if "liability" in query.lower():
            relevant_chunks = [c for c in chunks if "Liability" in c['text']]
        elif "gdpr" in query.lower() or "data" in query.lower():
            relevant_chunks = [c for c in chunks if "Data" in c['text']]
        else:
            relevant_chunks = [chunks[0], chunks[2]] # Fallback
            
        return {
            "found_clauses": relevant_chunks,
            "reasoning_steps": ["Identified intent", f"Retrieved {len(relevant_chunks)} clauses"]
        }

class DraftingAgent:
    """Synthesizes findings into a response."""
    async def draft(self, analysis_result: Dict) -> AgentResponse:
        print(f"[DraftingAgent] Composing response...")
        await asyncio.sleep(0.8)
        
        clauses = analysis_result["found_clauses"]
        if not clauses:
            return AgentResponse(
                answer="I could not find specific clauses related to your query.",
                citations=[], confidence=0.2, agent_trace=["Ingestion", "Vector", "Analysis (Failed)"]
            )
            
        intro = "Based on the analysis, here are the findings:\n\n"
        body = "".join([f"• **Section (Page {c['page']}):** {c['text']}\n" for c in clauses])
        
        return AgentResponse(
            answer=intro + body,
            citations=[c['page'] for c in clauses],
            confidence=0.95,
            agent_trace=["Ingestion", "Vector", "Analysis", "Drafting"]
        )

# Initialize singletons
ingest_agent = IngestionAgent()
vector_agent = VectorAgent()
analysis_agent = AnalysisAgent()
drafting_agent = DraftingAgent()

# --- FastAPI App ---
app = FastAPI(title="Legal Compliance AI Simulation")
router = APIRouter()

@router.post("/ingest/upload-document/")
async def upload_document(file: UploadFile):
    doc_id = str(uuid.uuid4())
    document_store[doc_id] = {"filename": file.filename, "status": "processing"}
    
    ingestion_result = await ingest_agent.process(file.filename)
    document_store[doc_id].update(ingestion_result)
    
    await vector_agent.embed_and_store(doc_id, ingestion_result["raw_text"])
    document_store[doc_id]["status"] = "ready"
    
    return {"document_id": doc_id, "filename": file.filename, "message": "Ingestion complete"}

@router.post("/analyze", response_model=AgentResponse)
async def analyze(request: AnalysisRequest):
    analysis_result = await analysis_agent.analyze(request.session_id, request.query)
    response = await drafting_agent.draft(analysis_result)
    return response

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)