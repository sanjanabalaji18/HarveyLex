from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai_modules.rewrite_agent import RewriteAgent
from ai_modules.regulation_finder import RegulationFinder

from datastore.embedding_utils import EmbeddingService

router = APIRouter()

rewriter = RewriteAgent()
finder = RegulationFinder()
embedder = EmbeddingService()


class RewriteRequest(BaseModel):
    clause: str
    issue: str # e.g., "Clause is too vague"
    context: str # e.g., "This is a contract for data processing"


@router.post("/drafting/rewrite-clause/")
async def rewrite_clause(req: RewriteRequest):
    """
    Rewrites a legal clause to be more compliant or clear.
    1. Finds a relevant regulation or best-practice example from the vector store.
    2. Uses a GenAI agent to rewrite the clause based on the example.
    """
    try:
        # 1. Embed the user's clause to find a relevant example
        query_embedding = embedder.embed_query(req.clause + " " + req.context)
        
        # 2. Search for the most relevant example in the vector store
        example_matches = finder.search(query_embedding, k=1)
        
        reference_text = ""
        if example_matches:
            # Use the text of the most relevant match as a reference
            reference_text = example_matches[0].get("text", "")

        # 3. Call the rewrite agent
        rewritten_suggestions = await rewriter.rewrite(
            clause=req.clause,
            issue=req.issue,
            reference_text=reference_text
        )

        return {
            "original_clause": req.clause,
            "issue": req.issue,
            "suggested_rewrites": rewritten_suggestions,
            "reference_used": reference_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rewrite failed: {str(e)}")
