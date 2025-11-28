from fastapi import APIRouter
from datastore.embedding_utils import EmbeddingService
from datastore.vector_store.faiss_store import FaissStore
from datastore.knowledge_repository import KnowledgeRepository

router = APIRouter()

embedder = EmbeddingService()
# Use the concrete FaissStore for health checks
try:
    vector_store = FaissStore()
except Exception:
    vector_store = None

# Inject vector_store into KnowledgeRepository so it delegates to the store
knowledge = KnowledgeRepository(vector_store=vector_store if vector_store is not None else None)


@router.get("/health")
async def health():
    # Determine vector store health
    vs_health = False
    if vector_store is not None:
        try:
            vs_health = vector_store.is_healthy()
        except Exception:
            vs_health = False

    # Count regulations/documents stored
    reg_count = 0
    try:
        if vector_store is not None and hasattr(vector_store, "metadata"):
            reg_count = len(getattr(vector_store, "metadata", []))
        elif hasattr(knowledge, "metadata"):
            reg_count = len(getattr(knowledge, "metadata", []))
    except Exception:
        reg_count = 0

    return {
        "status": "ok",
        "embedding_engine": getattr(embedder, "is_healthy", lambda: False)(),
        "vector_store": vs_health,
        "regulation_corpus": reg_count,
        "message": "All systems operational"
    }
