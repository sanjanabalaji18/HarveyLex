import os
from core.logger import get_logger
import google.generativeai as genai

class RewriteAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-pro")

    def rewrite_text(self, text: str, objective: str):
        """
        Rewrites legal/contract text based on the provided objective.
        For example:
        - simplify
        - formalize
        - make legally compliant
        - summarize
        """
        prompt = f"""
You are a legal rewriting assistant.

Objective: {objective}

Rewrite the following text accordingly. Preserve meaning and accuracy.

Text:
{text}
"""

        response = self.model.generate_content(prompt)
        return response.text
