from fastapi import APIRouter, UploadFile, HTTPException
import os

from legal_compliance_ai.ingestion.pdf_ingestion import PDFIngestion
from legal_compliance_ai.ingestion.chunking import Chunker
from legal_compliance_ai.embeddings.embedder import EmbeddingGenerator
from legal_compliance_ai.vector_store.faiss_store import VectorStore

router = APIRouter()

UPLOAD_DIR = "uploads/"


@router.post("/ingest")
async def ingest(file: UploadFile):

    try:
        # ---------------------------
        # 1. Save uploaded file
        # ---------------------------
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # ---------------------------
        # 2. Load ONLY this PDF → text
        # ---------------------------
        loader = PDFIngestion()
        texts = loader.read_pdf(file_path)

        if not texts:
            raise HTTPException(status_code=400, detail="PDF contains no extractable text.")

        # ---------------------------
        # 3. Chunk into passages
        # ---------------------------
        chunker = Chunker()
        chunks = chunker.chunk(texts)

        # ---------------------------
        # 4. Gemini embeddings
        # ---------------------------
        embedder = EmbeddingGenerator()
        embeddings = embedder.embed(chunks)

        if len(embeddings) == 0:
            raise HTTPException(status_code=500, detail="Embedding generation failed.")

        # ---------------------------
        # 5. Store vectors in FAISS
        # ---------------------------
        store = VectorStore(dim=len(embeddings[0]))
        store.add(embeddings)
        store.save()

        return {
            "status": "success",
            "uploaded_file": file.filename,
            "chunks_generated": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
