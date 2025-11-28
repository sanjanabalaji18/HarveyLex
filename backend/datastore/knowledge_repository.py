import numpy as np
import faiss
import os
from typing import Optional

from datastore.embedding_utils import EmbeddingService
from core.logger import get_logger
from datastore.vector_store.vector_store import VectorStore


logger = get_logger(__name__)


class KnowledgeRepository:
    """Repository abstraction that can use either an internal FAISS index
    or an external VectorStore implementation (dependency-injected).

    If `vector_store` is provided, the repository will delegate storage and
    search operations to it. Otherwise it will maintain a local FAISS index.
    """

    def __init__(self, vector_store: Optional[VectorStore] = None):
        self.embedding_service = EmbeddingService()
        
        # Default to the persistent FaissStore if no store is provided
        if vector_store is None:
            from datastore.vector_store.faiss_store import FaissStore
            self.vector_store = FaissStore()
        else:
            self.vector_store = vector_store

        # Ensure vector store folder exists (used by the internal index path)
        self.store_path = "datastore/vector_store"
        os.makedirs(self.store_path, exist_ok=True)

        # We no longer rely on internal FAISS index as primary, but keep it for fallback if needed
        # or just rely entirely on vector_store which is now always present.
        self.index = None 
        self.metadata = []

    async def add_document(self, text: str, doc_id: str):
        """Embed and store text chunks in the vector store."""
        logger.info(f"Adding document chunk for doc_id: {doc_id}")
        embedding = await self.embedding_service.embed_text(text)

        if self.vector_store is not None:
            # vector_store expects documents with 'text', 'embedding', and metadata
            doc = {
                "text": text,
                "embedding": embedding,
                "metadata": {"doc_id": doc_id}
            }
            # Some vector stores expose synchronous add_documents
            try:
                self.vector_store.add_documents([doc])
            except Exception:
                # Fallback to any async variant
                try:
                    import asyncio
                    asyncio.get_event_loop().run_until_complete(self.vector_store.add_documents([doc]))
                except Exception:
                    logger.exception("Failed to add document to vector_store")
        
        logger.info(f"Successfully added document chunk for doc_id: {doc_id}")

    async def search(self, query: str, top_k: int = 5):
        """Return nearest matches from vector_store."""
        logger.info(f"Searching for query: '{query}' with top_k={top_k}")
        query_vec = await self.embedding_service.embed_text(query)

        if self.vector_store is not None:
            try:
                return self.vector_store.search(query_vec, k=top_k)
            except Exception:
                try:
                    import asyncio
                    return asyncio.get_event_loop().run_until_complete(self.vector_store.search_async(query_vec, k=top_k))
                except Exception:
                    logger.exception("Vector store search failed")
                    return []
        return []

    def get_document_text(self, doc_id: str) -> str:
        """Retrieve text for a specific document ID."""
        if self.vector_store and hasattr(self.vector_store, "get_document_by_id"):
            doc = self.vector_store.get_document_by_id(doc_id)
            if doc:
                return doc.get("text", "")
        
        # Fallback to internal metadata if used (legacy)
        for item in self.metadata:
            if item.get("doc_id") == doc_id:
                return item.get("text", "")
        
        return ""
