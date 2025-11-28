from typing import List
from backend.core.logger import get_logger



class TextSplitter:
    """
    Simple but effective text splitter for legal documents.
    Splits by sentence blocks with overlap.
    """

    def __init__(self, chunk_size=450, overlap=80):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> List[str]:
        text = text.strip()
        if not text:
            return []

        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = start + self.chunk_size
            segment = words[start:end]
            chunks.append(" ".join(segment))

            # move forward but include overlap
            start += (self.chunk_size - self.overlap)

        return chunks
