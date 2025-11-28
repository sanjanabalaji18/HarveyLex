import google.generativeai as genai
import numpy as np
from typing import List, Union
import os
from dotenv import load_dotenv

load_dotenv()


class Embedder:
    """
    Embedding generator using Gemini AI for text vectorization.
    """

    def __init__(self, model_name: str = "models/embedding-001", dimension: int = 768):
        api_key = os.getenv("AIzaSyBzyf2zMEQ_kq8N0w2mF7yfnraX45oDtiw")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = model_name
        else:
            self.model = None
        self.dimension = dimension

    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        """
        if not self.model:
            # Return random vector if API not configured
            return np.random.rand(self.dimension).astype(np.float32)

        try:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            return np.array(result['embedding'], dtype=np.float32)
        except Exception as e:
            print(f"Embedding failed: {e}")
            return np.random.rand(self.dimension).astype(np.float32)

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts.
        """
        if not self.model:
            return np.random.rand(len(texts), self.dimension).astype(np.float32)

        embeddings = []
        for text in texts:
            embedding = self.embed_text(text)
            embeddings.append(embedding)

        return np.array(embeddings, dtype=np.float32)

    def similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2) if norm1 != 0 and norm2 != 0 else 0.0

    def is_available(self) -> bool:
        """
        Check if the embedding service is available.
        """
        return self.model is not None
