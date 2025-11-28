
import sys
import os
import asyncio

# Add current directory to path so imports work as if running from backend/
sys.path.append(os.getcwd())

print("Checking imports...")

try:
    from main import app
    print("✅ main imported")
    
    from api.routes_ingestion import router as ingestion_router
    print("✅ routes_ingestion imported")
    
    from api.routes_analysis import router as analysis_router
    print("✅ routes_analysis imported")
    
    from api.routes_drafting import router as drafting_router
    print("✅ routes_drafting imported")
    
    from api.routes_health import router as health_router
    print("✅ routes_health imported")

    from ai_modules.document_classifier import DocumentClassifier
    print("✅ document_classifier imported")

    from ai_modules.regulation_finder import RegulationFinder
    print("✅ regulation_finder imported")

    from ai_modules.summary_agent import SummaryAgent
    print("✅ summary_agent imported")

    from ai_modules.rewrite_agent import RewriteAgent
    print("✅ rewrite_agent imported")
    
    from datastore.pdf_reader import PDFReader
    print("✅ pdf_reader imported")
    
    from datastore.text_splitter import TextSplitter
    print("✅ text_splitter imported")
    
    from datastore.embedding_utils import EmbeddingService
    print("✅ embedding_utils imported")
    
    from datastore.vector_store.faiss_store import FaissStore
    print("✅ faiss_store imported")
    
    from datastore.knowledge_repository import KnowledgeRepository
    print("✅ knowledge_repository imported")

    print("\n🎉 All modules imported successfully! Syntax and imports look good.")

except Exception as e:
    print(f"\n❌ Import Error: {e}")
    sys.exit(1)
