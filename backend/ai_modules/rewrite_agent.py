import os
from core.logger import get_logger
import google.generativeai as genai

class RewriteAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-pro")

    async def rewrite(self, clause: str, issue: str, context: str, reference_text: str = ""):
        """
        Rewrites a legal clause to address a specific issue.
        """
        prompt = f"""
        You are a senior legal drafter.
        Rewrite the following clause to address the issue described.
        
        CONTEXT:
        {context}

        ORIGINAL CLAUSE:
        {clause}

        ISSUE TO FIX:
        {issue}

        REFERENCE / PRECEDENT (Optional):
        {reference_text}

        Provide 3 distinct options for the rewrite:
        1. Conservative (Minimal change)
        2. Balanced (Standard market practice)
        3. Aggressive (Strongly favoring the party)
        """

        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            get_logger(__name__).error(f"Rewrite failed: {e}")
            return "Error generating rewrite."
