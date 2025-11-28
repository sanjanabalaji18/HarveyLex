import os
import json
from typing import List, Dict, Any

import numpy as np

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
        vectors_np = np.array(vectors, dtype=np.float32)
        self.add(vectors_np, metadata)

    async def search_async(self, query_embedding, k: int = 5):
        return self.search(query_embedding, k)
import os
import numpy as np
import faiss
import json
from typing import List, Dict, Any, Optional


class VectorStore:
    """
    FAISS-based vector store for document chunks and embeddings.
    Handles storage, retrieval, and persistence of vector data.
    """

    def __init__(self, dim: int = 768, index_file: str = "faiss_index.idx", metadata_file: str = "store_metadata.json"):
        self.dim = dim
        self.index_file = index_file
        self.metadata_file = metadata_file
        self.index = faiss.IndexFlatIP(dim)  # Inner product for cosine similarity
        import os
        import numpy as np
        import faiss
        import json
        from typing import List, Dict, Any, Optional


        class VectorStore:
            """
            FAISS-based vector store for document chunks and embeddings.
            Handles storage, retrieval, and persistence of vector data.
            """

            def __init__(self, dim: int = 768, index_file: str = "faiss_index.idx", metadata_file: str = "store_metadata.json"):
                self.dim = dim
                self.index_file = index_file
                self.metadata_file = metadata_file
                self.index = faiss.IndexFlatIP(dim)  # Inner product for cosine similarity
                self.metadata: List[Dict[str, Any]] = []
                self.load()

            def add(self, vectors: np.ndarray, metadata: List[Dict[str, Any]] = None):
                """
                Add vectors to the store with optional metadata.
                """
                if vectors.shape[1] != self.dim:
                    raise ValueError(f"Vector dimension {vectors.shape[1]} does not match store dimension {self.dim}")

                import os
                import numpy as np
                import faiss
                import json
                from typing import List, Dict, Any, Optional


                class VectorStore:
                    """
                    FAISS-based vector store for document chunks and embeddings.
                    Handles storage, retrieval, and persistence of vector data.
                    """

                    def __init__(self, dim: int = 768, index_file: str = "faiss_index.idx", metadata_file: str = "store_metadata.json"):
                        self.dim = dim
                        self.index_file = index_file
                        self.metadata_file = metadata_file
                        self.index = faiss.IndexFlatIP(dim)  # Inner product for cosine similarity
                        self.metadata: List[Dict[str, Any]] = []
                        self.load()

                    def add(self, vectors: np.ndarray, metadata: List[Dict[str, Any]] = None):
                        """
                        Add vectors to the store with optional metadata.
                        """
                        if vectors.shape[1] != self.dim:
                            raise ValueError(f"Vector dimension {vectors.shape[1]} does not match store dimension {self.dim}")

                        self.index.add(vectors)

                        if metadata:
                            for i, meta in enumerate(metadata):
                                meta["vector_index"] = len(self.metadata) + i
                                self.metadata.append(meta)

                        self.save()

                    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
                        """
                        Search for similar vectors.
                        """
                        query_vector = np.array([query_vector], dtype=np.float32)
                        distances, indices = self.index.search(query_vector, k)

                        results = []
                        for dist, idx in zip(distances[0], indices[0]):
                            if idx < len(self.metadata):
                                result = self.metadata[idx].copy()
                                result["similarity"] = float(dist)
                                results.append(result)

                        return results

                    def save(self):
                        """
                        Save the index and metadata to disk.
                        """
                        faiss.write_index(self.index, self.index_file)
                        with open(self.metadata_file, 'w') as f:
                            json.dump(self.metadata, f, indent=2)

                    def load(self):
                        """
                        Load the index and metadata from disk if they exist.
                        """
                        if os.path.exists(self.index_file):
                            try:
                                self.index = faiss.read_index(self.index_file)
                            except Exception:
                                # If loading fails, reinitialize an empty index
                                self.index = faiss.IndexFlatIP(self.dim)
                        if os.path.exists(self.metadata_file):
                            with open(self.metadata_file, 'r') as f:
                                self.metadata = json.load(f)

                    def is_healthy(self) -> bool:
                        """
                        Health check for the vector store.
                        """
                        return self.index.ntotal == len(self.metadata)

                    def clear(self):
                        """
                        Clear all data from the store.
                        """
                        self.index = faiss.IndexFlatIP(self.dim)
                        self.metadata = []
                        self.save()


                # Backwards-compatible FaissStore wrapper expected by other modules
                class FaissStore(VectorStore):
                    """
                    Compatibility wrapper exposing the older/expected API:
                    - Accepts `index_path` and `store_path` kwargs for callers that expect
                      those names.
                    - `add_documents(documents: List[dict])` where each dict contains
                      'text', 'embedding', and optional 'metadata'.
                    - `async def search(query_embedding, k=5)` to support callers that
                      `await` the search result.
                    """
                    def __init__(self, index_path: str = "faiss_index.bin", store_path: str = "text_store.json", dimension: int = 768):
                        # Map legacy names to current parameter names
                        super().__init__(dim=dimension, index_file=index_path, metadata_file=store_path)

                    def add_documents(self, documents):
                        if not documents:
                            return
                        vectors = [d['embedding'] for d in documents]
                        vectors_np = np.array(vectors, dtype=np.float32)
                        metadata = [d.get('metadata') for d in documents]
                        self.add(vectors_np, metadata)

                    async def search(self, query_embedding, k: int = 5):
                        # run the synchronous search and return result (kept async for callers)
                        return self.search_sync(query_embedding, k)

                    def search_sync(self, query_embedding, k: int = 5):
                        return super().search(query_embedding, k)
