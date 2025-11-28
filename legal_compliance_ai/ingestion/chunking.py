from typing import List


class Chunker:
    """
    Text chunking utility for splitting documents into manageable pieces.
    Supports different chunking strategies for legal documents.
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        """
        Split text into chunks with overlap.
        """
        if not text or not text.strip():
            return []

        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = start + self.chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)
            chunks.append(chunk_text)

            # Move start position with overlap
            start += (self.chunk_size - self.overlap)

            # Prevent infinite loop
            if start >= len(words):
                break

        return chunks

    def chunk_by_sentences(self, text: str, max_sentences: int = 3) -> List[str]:
        """
        Chunk text by sentences, grouping multiple sentences together.
        """
        import re

        # Split by sentence endings
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())

        chunks = []
        current_chunk = []

        for sentence in sentences:
            current_chunk.append(sentence)

            if len(current_chunk) >= max_sentences:
                chunks.append(" ".join(current_chunk))
                current_chunk = current_chunk[-1:]  # Keep last sentence for overlap

        # Add remaining sentences
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def chunk_by_paragraphs(self, text: str, max_paragraphs: int = 2) -> List[str]:
        """
        Chunk text by paragraphs.
        """
        paragraphs = text.split('\n\n')

        chunks = []
        current_chunk = []

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            current_chunk.append(para)

            if len(current_chunk) >= max_paragraphs:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []

        # Add remaining paragraphs
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks

    def smart_chunk(self, text: str) -> List[str]:
        """
        Intelligent chunking that tries to preserve document structure.
        """
        # First try paragraph-based chunking
        chunks = self.chunk_by_paragraphs(text)

        # If chunks are too small, fall back to sentence-based
        if chunks and len(chunks[0].split()) < 100:
            chunks = self.chunk_by_sentences(text)

        # If still too small, fall back to word-based
        if chunks and len(chunks[0].split()) < 100:
            chunks = self.chunk(text)

        return chunks
