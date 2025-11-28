import sys
import os
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Mock google.generativeai before importing modules that use it
sys.modules["google.generativeai"] = MagicMock()

from backend.datastore.knowledge_repository import KnowledgeRepository
from backend.ai_modules.document_classifier import DocumentClassifier
from backend.ai_modules.summary_agent import SummaryAgent

async def test_integration():
    print("Starting integration verification...")

    # 1. Test KnowledgeRepository and FaissStore integration
    print("Testing KnowledgeRepository...")
    repo = KnowledgeRepository()
    
    # Mock embedding service to avoid API calls
    repo.embedding_service.embed_text = AsyncMock(return_value=[0.1] * 768)
    
    doc_id = "test-doc-123"
    text = "This is a legal contract for testing purposes."
    
    await repo.add_document(text, doc_id)
    
    retrieved_text = repo.get_document_text(doc_id)
    if retrieved_text == text:
        print("✅ KnowledgeRepository.get_document_text passed")
    else:
        print(f"❌ KnowledgeRepository.get_document_text failed. Got: '{retrieved_text}'")

    # 2. Test DocumentClassifier
    print("Testing DocumentClassifier...")
    classifier = DocumentClassifier()
    # Mock model response
    classifier.model.generate_content.return_value.text = "contract"
    
    category = classifier.classify_document(text)
    if category == "contract":
        print("✅ DocumentClassifier passed")
    else:
        print(f"❌ DocumentClassifier failed. Got: '{category}'")

    # 3. Test SummaryAgent
    print("Testing SummaryAgent...")
    agent = SummaryAgent()
    # Mock model responses
    agent.model_pro.generate_content.return_value.text = "Legal Summary"
    agent.model_flash.generate_content.return_value.text = "Basic Summary"
    
    # Test legal summary
    summary = agent.summarize(text, [{"text": "clause 1"}])
    if summary == "Legal Summary":
        print("✅ SummaryAgent.summarize passed")
    else:
        print(f"❌ SummaryAgent.summarize failed. Got: '{summary}'")

    # Test basic summary
    basic = agent.basic_summary(text)
    if basic == "Basic Summary":
        print("✅ SummaryAgent.basic_summary passed")
    else:
        print(f"❌ SummaryAgent.basic_summary failed. Got: '{basic}'")

    print("Verification complete.")

if __name__ == "__main__":
    asyncio.run(test_integration())
