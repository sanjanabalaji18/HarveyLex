import google.generativeai as genai
from backend.datastore.knowledge_repository import KnowledgeRepository

from backend.ai_modules.reasoning_unit import ReasoningUnit
from backend.ai_modules.document_inspector import DocumentInspector

import os
from dotenv import load_dotenv

load_dotenv()

class ComplianceEngine:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.repo = KnowledgeRepository()
        self.reasoner = ReasoningUnit()

    async def run_full_compliance_check(self, clause: str):
        # 1. Retrieve relevant legal chunks
        matches = self.repo.search(clause)

        # 2. Ask Gemini to perform deep legal reasoning
        analysis = await self.reasoner.evaluate_clause(clause, matches)

        return {
            "input_clause": clause,
            "matches": matches,
            "analysis": analysis
        }
