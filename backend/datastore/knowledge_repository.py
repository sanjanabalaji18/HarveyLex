import numpy as np
import faiss
import os
from typing import Optional

from backend.datastore.embedding_utils import EmbeddingService
from backend.core.logger import get_logger
from backend.datastore.vector_store.vector_store import VectorStore


logger = get_logger(__name__)


class KnowledgeRepository:
    """Repository abstraction that can use either an internal FAISS index
    or an external VectorStore implementation (dependency-injected).

    If `vector_store` is provided, the repository will delegate storage and
    search operations to it. Otherwise it will maintain a local FAISS index.
    """

    def __init__(self, vector_store: Optional[VectorStore] = None):
        self.embedding_service = EmbeddingService()
        self.vector_store = vector_store

        # Ensure vector store folder exists (used by the internal index path)
        self.store_path = "datastore/vector_store"
        os.makedirs(self.store_path, exist_ok=True)

        if self.vector_store is None:
            # Internal FAISS fallback (768 dims)
            self.index = faiss.IndexFlatL2(768)
            self.metadata = []

    async def add_document(self, text: str, doc_id: str):
        """Embed and store text chunks either in the injected vector store
        or in the internal FAISS index.
        """
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
        else:
            vec = np.array([embedding], dtype="float32")
            self.index.add(vec)
            self.metadata.append({"doc_id": doc_id, "text": text})

        logger.info(f"Successfully added document chunk for doc_id: {doc_id}")

    async def search(self, query: str, top_k: int = 5):
        """Return nearest matches either from injected vector_store or internal index."""
        logger.info(f"Searching for query: '{query}' with top_k={top_k}")
        query_vec = await self.embedding_service.embed_text(query)

        if self.vector_store is not None:
            # delegate to the vector store. Ensure we pass an embedding
            try:
                return self.vector_store.search(query_vec, k=top_k)
            except Exception:
                # try async search helper if provided
                try:
                    import asyncio

                    return asyncio.get_event_loop().run_until_complete(self.vector_store.search_async(query_vec, k=top_k))
                except Exception:
                    logger.exception("Vector store search failed")
                    return []

        query_vec = np.array([query_vec], dtype="float32")
        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        logger.info(f"Found {len(results)} results for query: '{query}'")
        return results
