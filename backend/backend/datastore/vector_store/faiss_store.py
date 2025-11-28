
import os
import json
import faiss
import numpy as np
from typing import List, Tuple, Dict, Any

class FaissStore:
    """
    A FAISS-based vector store for efficient similarity search.

    This class manages a FAISS index for vector embeddings and a separate
    JSON file for storing the corresponding text content and metadata. It
    handles creating, loading, and saving both the index and the text store,
    ensuring data persistence.
    """
    def __init__(self, index_path: str = "faiss_index.bin", store_path: str = "text_store.json", dimension: int = 768):
        """
        Initializes the FaissStore, loading existing data or creating new files.

        Args:
            index_path (str): Path to the FAISS index file.
            store_path (str): Path to the JSON file for text and metadata.
            dimension (int): The dimensionality of the vectors (e.g., 768 for many sentence-transformers).
        """
        self.index_path = index_path
        self.store_path = store_path
        self.dimension = dimension

        self.index = self._load_index()
        self.store: Dict[str, Dict[str, Any]] = self._load_store()

    def _load_index(self):
        """Loads the FAISS index from disk if it exists, otherwise creates a new one."""
        if os.path.exists(self.index_path):
            print(f"Loading FAISS index from {self.index_path}")
            return faiss.read_index(self.index_path)
        else:
            print(f"Creating new FAISS index of dimension {self.dimension}")
            return faiss.IndexFlatL2(self.dimension)

    def _load_store(self) -> Dict[str, Dict[str, Any]]:
        """Loads the text store from disk if it exists, otherwise returns an empty dictionary."""
        if os.path.exists(self.store_path):
            print(f"Loading text store from {self.store_path}")
            with open(self.store_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_index(self):
        """Saves the FAISS index to disk."""
        print(f"Saving FAISS index to {self.index_path}")
        faiss.write_index(self.index, self.index_path)

    def _save_store(self):
        """Saves the text store to disk."""
        print(f"Saving text store to {self.store_path}")
        with open(self.store_path, 'w', encoding='utf-8') as f:
            json.dump(self.store, f, indent=4)

    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Adds multiple documents with their embeddings to the store.

        This is the primary method for adding data. It expects each document
        to have 'text', 'embedding', and 'metadata'.

        Args:
            documents (List[Dict[str, Any]]): A list of documents to add.
                                               Each dict must have 'text', 'embedding',
                                               and 'metadata' keys.
        """
        if not documents:
            return

        embeddings = [doc['embedding'] for doc in documents]
        
        # Ensure embeddings are float32 and normalized for some index types if needed
        embeddings_np = np.array(embeddings, dtype='float32')

        # Add vectors to the FAISS index
        self.index.add(embeddings_np)

        # Add text and metadata to the store
        start_index = len(self.store)
        for i, doc in enumerate(documents):
            doc_id = str(start_index + i)
            self.store[doc_id] = {
                "text": doc['text'],
                "metadata": doc.get('metadata', {})
            }
        
        # Persist changes to disk
        self._save_index()
        self._save_store()

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        """
        Searches the vector store for the most similar documents.

        Args:
            query_embedding (np.ndarray): The embedding of the query text.
            k (int): The number of similar documents to return.

        Returns:
            List[Dict[str, Any]]: A list of search results, each containing
                                   the 'text', 'metadata', and 'score'.
        """
        if self.index.ntotal == 0:
            return []

        query_embedding_np = np.array([query_embedding], dtype='float32')
        
        # Perform the search
        distances, indices = self.index.search(query_embedding_np, k)

        results = []
        for i in range(indices.shape[1]):
            doc_id = str(indices[0, i])
            if doc_id in self.store:
                results.append({
                    "text": self.store[doc_id]['text'],
                    "metadata": self.store[doc_id]['metadata'],
                    "score": float(distances[0, i])
                })
        return results

    def get_document_by_id(self, doc_id: str) -> Dict[str, Any]:
        """
        Retrieves a document by its ID.

        Args:
            doc_id (str): The ID of the document to retrieve.

        Returns:
            A dictionary containing the document's text and metadata, or None.
        """
        return self.store.get(doc_id)

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Retrieves all documents from the store.

        Returns:
            A list of all documents.
        """
        return list(self.store.values())

    def clear(self):
        """
        Clears the entire vector store, deleting index and store files.
        """
        # Reset in-memory state
        self.index = faiss.IndexFlatL2(self.dimension)
        self.store = {}

        # Delete files from disk
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
            print(f"Deleted {self.index_path}")
        if os.path.exists(self.store_path):
            os.remove(self.store_path)
            print(f"Deleted {self.store_path}")

        print("Vector store cleared.")

