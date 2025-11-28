import os
import numpy as np
from typing import List
from dotenv import load_dotenv
from backend.core.logger import get_logger

# Load .env if present
load_dotenv()

try:
    import google.generativeai as genai
except Exception:
    genai = None


class EmbeddingService:
    """
    Generates dense embeddings using the Gemini embedding API.
    Written to be simple, stable, and competition-ready.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        # If no API key, system still runs with fallback embeddings
        if api_key and genai:
            genai.configure(api_key=api_key)
            self.engine_ready = True
        else:
            self.engine_ready = False

        # Use a standard dimension to maintain consistency
        self.default_dim = 768

    def embed_text(self, text: str) -> np.ndarray:
        """
        Embed a single piece of text.

        Returns a numpy vector. Falls back to deterministic hashing
        when no API key is found.
        """
        text = text.strip()
        if not text:
            return np.zeros(self.default_dim)

        if self.engine_ready:
            try:
                response = genai.embed_content(
                    model="models/text-embedding-004",
                    content=text
                )
                vec = response.get("embedding", [])
                return np.array(vec, dtype=float)
            except Exception:
                # If API fails, fallback kicks in
                return self._fallback_vector(text)

        # No Gemini key → fallback embedding
        return self._fallback_vector(text)

    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """
        Embed a batch of texts.
        """
        vectors = []
        for t in texts:
            vectors.append(self.embed_text(t))
        return vectors

    def _fallback_vector(self, text: str) -> np.ndarray:
        """
        Deterministic hashing fallback.
        Ensures stable results without an API key.
        """
        seed = abs(hash(text)) % (10**6)
        rng = np.random.default_rng(seed)
        return rng.normal(0, 1, self.default_dim).astype(float)

    def is_healthy(self) -> bool:
        """Simple health check for diagnostics."""
        return self.engine_ready
