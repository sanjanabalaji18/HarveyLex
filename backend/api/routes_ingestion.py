from fastapi import APIRouter, UploadFile, HTTPException
from backend.datastore.pdf_reader import PDFReader
# Use the FAISS-backed concrete vector store implementation
from backend.datastore.vector_store.faiss_store import FaissStore as FaissVectorStore

from backend.datastore.text_splitter import TextSplitter
from backend.datastore.embedding_utils import EmbeddingService

from backend.datastore.knowledge_repository import KnowledgeRepository
import uuid
import os

router = APIRouter()

# Instantiate core ingestion tools
reader = PDFReader()
splitter = TextSplitter()
embedder = EmbeddingService()
vector_store = FaissVectorStore()


UPLOAD_DIR = "datastore/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/ingest/upload-document/")
async def upload_document(file: UploadFile):
    """
    Full ingestion pipeline:
    1. Save file to temp location
    2. Extract clean, readable text
    3. Chunk the text into manageable segments
    4. Generate embeddings for each chunk
    5. Add the chunks and their embeddings to the vector store
    """
    try:
        # Save the uploaded file temporarily
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 1. Extract text content from the document
        # This reader needs to handle different file types (pdf, docx, etc.)
        text = reader.extract(file_path, file.content_type)
        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from document.")

        # 2. Chunk the text into smaller segments
        chunks = splitter.split(text)
        if not chunks:
            raise HTTPException(status_code=400, detail="Text splitting resulted in no chunks.")

        # 3. Generate embeddings for each chunk
        embeddings = embedder.embed_batch(chunks)
        if not embeddings:
            raise HTTPException(status_code=500, detail="Embedding generation failed.")

        # 4. Prepare documents for the vector store
        doc_id = str(uuid.uuid4())
        documents_to_add = [
            {
                "text": chunk,
                "embedding": emb,
                "metadata": {"document_id": doc_id, "filename": file.filename}
            }
            for chunk, emb in zip(chunks, embeddings)
        ]

        # 5. Add documents to the FaissStore
        vector_store.add_documents(documents_to_add)

        return {
            "document_id": doc_id,
            "filename": file.filename,
            "message": f"Successfully ingested {len(chunks)} chunks."
        }

    except Exception as e:
        # Clean up the saved file in case of an error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"An error occurred during ingestion: {str(e)}")
