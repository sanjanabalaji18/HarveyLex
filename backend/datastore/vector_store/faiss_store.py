import os
import json
from typing import List, Dict, Any, Optional

import numpy as np

from datastore.vector_store.vector_store import VectorStore
from core.logger import get_logger

try:
    import faiss
except Exception:
    faiss = None  # faiss may not be installed in all environments


class VectorStore:
    """Simple FAISS-backed vector store with persistence."""

    def __init__(self, dim: int = 768, index_file: str = "faiss_index.idx", metadata_file: str = "store_metadata.json"):
        self.dim = dim
        self.index_file = index_file
        self.metadata_file = metadata_file
        if faiss is None:
            raise RuntimeError("faiss is not available in this environment")
        self.index = faiss.IndexFlatIP(dim)
        self.metadata: List[Dict[str, Any]] = []
        self.load()

    def add(self, vectors: np.ndarray, metadata: List[Dict[str, Any]] = None):
        if vectors.ndim == 1:
            vectors = np.array([vectors], dtype=np.float32)
        vectors = np.asarray(vectors, dtype=np.float32)
        if vectors.shape[1] != self.dim:
            raise ValueError("embedding dimension mismatch")
        self.index.add(vectors)
        if metadata:
            for i, meta in enumerate(metadata):
                meta = meta or {}
                meta["vector_index"] = len(self.metadata) + i
                self.metadata.append(meta)
        self.save()

    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        q = np.asarray([query_vector], dtype=np.float32)
        distances, indices = self.index.search(q, k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata):
                item = dict(self.metadata[idx])
                item["similarity"] = float(dist)
                results.append(item)
        return results

    def save(self):
        try:
            faiss.write_index(self.index, self.index_file)
        except Exception:
            pass
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def load(self):
        if faiss is None:
            return
        if os.path.exists(self.index_file):
            try:
                self.index = faiss.read_index(self.index_file)
            except Exception:
                self.index = faiss.IndexFlatIP(self.dim)
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r") as f:
                try:
                    self.metadata = json.load(f)
                except Exception:
                    self.metadata = []


class FaissStore(VectorStore):
    """Compatibility wrapper exposing expected legacy kwargs and helper methods."""

    def __init__(self, index_path: str = "faiss_index.idx", store_path: str = "store_metadata.json", dimension: int = 768):
        super().__init__(dim=dimension, index_file=index_path, metadata_file=store_path)

    def add_documents(self, documents: List[Dict[str, Any]]):
        if not documents:
            return
        vectors = [d["embedding"] for d in documents]
        metadata = [d.get("metadata", {}) for d in documents]
        # Ensure metadata contains the text if it's not already there but is in the document
        for i, doc in enumerate(documents):
            if "text" in doc and "text" not in metadata[i]:
                metadata[i]["text"] = doc["text"]
                
        vectors_np = np.array(vectors, dtype=np.float32)
        self.add(vectors_np, metadata)

    async def search_async(self, query_embedding, k: int = 5):
        return self.search(query_embedding, k)

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a document by its ID from metadata."""
        for item in self.metadata:
            # Check both 'doc_id' and 'document_id' keys as usage varies
            if item.get("doc_id") == doc_id or item.get("document_id") == doc_id:
                return item
        return None
