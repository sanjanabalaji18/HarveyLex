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

    def __init__(self, dimension: int = 768, index_file: str = "vector_store.index", metadata_file: str = "metadata.json"):
        self.dimension = dimension
        self.index_file = index_file
        self.metadata_file = metadata_file
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.metadata: List[Dict[str, Any]] = []
        self.load()

    def add_document(self, document_id: str, chunks: List[str], embeddings: List[np.ndarray]):
        """
        Add a document's chunks and embeddings to the store.
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")

        vectors = np.array(embeddings, dtype=np.float32)
        self.index.add(vectors)

        for i, chunk in enumerate(chunks):
            self.metadata.append({
                "document_id": document_id,
                "chunk_index": i,
                "text": chunk,
                "vector_index": len(self.metadata)
            })

        self.save()

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors and return metadata.
        """
        query_vector = np.array([query_vector], dtype=np.float32)
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result["similarity"] = float(dist)
                results.append(result)

        return results

    def get_document(self, document_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all chunks for a specific document.
        """
        return [item for item in self.metadata if item["document_id"] == document_id]

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
            self.index = faiss.read_index(self.index_file)
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)

    def is_healthy(self) -> bool:
        """
        Health check for the vector store.
        """
        return self.index.ntotal == len(self.metadata)
