from typing import List, Dict, Any
import numpy as np

from datastore.embedding_utils import EmbeddingService
from datastore.knowledge_repository import KnowledgeRepository
from datastore.vector_store.vector_store import VectorStore
from datastore.vector_store.faiss_store import FaissStore


class RegulationFinder:
    """
    A module dedicated to retrieving relevant regulations from the FAISS-based vector store.
    """

    def __init__(self, index_path: str = "faiss_index.bin", store_path: str = "text_store.json"):
        """
        Initialize the RegulationFinder with:
        - Vector store (FAISS)
        - Embedding service
        - Knowledge repository wrapper
        """
        self.embedding_service = EmbeddingService()
        self.vector_store: VectorStore = FaissStore(
            index_path=index_path,
            store_path=store_path
        )
        self.knowledge_repo = KnowledgeRepository(self.vector_store)

    async def encode_query(self, query: str) -> np.ndarray:
        """
        Convert text to embedding using the embedding service.
        """
        embedding = await self.embedding_service.embed_text(query)
        return np.array(embedding, dtype=np.float32)

    async def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Semantic search over regulations using FAISS vector index.

        Args:
            query (str): Natural-language query from the user.
            k (int): Number of related regulations to return.

        Returns:
            List of matching regulation segments with metadata.
        """
        if not query:
            return []

        # Step 1: Convert query → embedding
        embedding = await self.encode_query(query)

        # Step 2: Perform vector search
        results = await self.vector_store.search_async(embedding, k)

        # Step 3: Format results
        return [
            {
                "doc_id": item.get("doc_id"),
                "text": item.get("text"),
            }
            for item in results
        ]
