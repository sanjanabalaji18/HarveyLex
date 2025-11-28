import numpy as np
import faiss
import os

from backend.datastore.embedding_utils import EmbeddingService
from core.logger import get_logger

logger = get_logger(__name__)

class KnowledgeRepository:
    def __init__(self):
        self.embedding_service = EmbeddingService()

        # Ensure vector store folder exists
        self.store_path = "datastore/vector_store"
        os.makedirs(self.store_path, exist_ok=True)

        # FAISS index: 768 dims (for Gemini embeddings)
        self.index = faiss.IndexFlatL2(768)
        self.metadata = []  # store simple Python dicts

    async def add_document(self, text: str, doc_id: str):
        """Embed and store text chunks."""
        logger.info(f"Adding document chunk for doc_id: {doc_id}")
        embedding = await self.embedding_service.embed_text(text)
        vector = np.array([embedding], dtype="float32")

        self.index.add(vector)
        self.metadata.append({"doc_id": doc_id, "text": text})
        logger.info(f"Successfully added document chunk for doc_id: {doc_id}")

    async def search(self, query: str, top_k: int = 5):
        """Return nearest matches"""
        logger.info(f"Searching for query: '{query}' with top_k={top_k}")
        query_vec = await self.embedding_service.embed_text(query)
        query_vec = np.array([query_vec], dtype="float32")

        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        
        logger.info(f"Found {len(results)} results for query: '{query}'")
        return results
