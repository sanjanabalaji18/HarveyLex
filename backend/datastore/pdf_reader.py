import io
from typing import Optional
import PyPDF2
try:
    from docx import Document
except ImportError as e:
    raise ImportError(
        "Missing dependency 'python-docx'. Install it with `pip install python-docx` "
        "or add `python-docx` to `backend/requirements.txt` and install requirements.") from e


class PDFReader:
    """
    Responsible for extracting text from uploaded documents.
    Supports PDF, DOCX, TXT.
    """

    def extract(self, data: bytes, content_type: str) -> str:
        content_type = (content_type or "").lower()

        if "pdf" in content_type:
            return self._read_pdf(data)

        if "word" in content_type or "docx" in content_type:
            return self._read_docx(data)

        # fallback to standard UTF decoding
        return self._read_text(data)

    def _read_pdf(self, data: bytes) -> str:
        try:
            pdf_stream = io.BytesIO(data)
            reader = PyPDF2.PdfReader(pdf_stream)
            pages = []

            for page in reader.pages:
                extracted = page.extract_text() or ""
                # Remove null bytes that some PDFs have
                extracted = extracted.replace('\x00', '')
                pages.append(extracted)

            return "\n".join(pages)

        except Exception:
            return ""

    def _read_docx(self, data: bytes) -> str:
        try:
            doc_stream = io.BytesIO(data)
            doc = Document(doc_stream)
            paragraphs = [p.text for p in doc.paragraphs]
            return "\n".join(paragraphs)
        except Exception:
            return ""

    def _read_text(self, data: bytes) -> str:
        try:
            return data.decode("utf-8", errors="ignore")
        except Exception:
            return ""
