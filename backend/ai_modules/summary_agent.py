import google.generativeai as genai
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class SummaryAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model_pro = genai.GenerativeModel("gemini-2.0-flash")
            self.model_flash = genai.GenerativeModel("gemini-2.0-flash")
        else:
            self.model_pro = None
            self.model_flash = None

    def summarize(self, text: str, vector_hits: List[Dict[str, Any]], query: str = None) -> str:
        if not self.model_pro:
            return "Summarizer not configured."

        # Extract text from vector hits
        context = "\n\n".join([hit.get("text", "") for hit in vector_hits])

        if query:
            prompt = f"""
            You are a legal analysis AI.
            Answer the user's query based on the document and relevant clauses provided.

            DOCUMENT CONTEXT:
            {text[:8000]}

            RELEVANT CLAUSES:
            {context}

            USER QUERY:
            {query}

            Provide a precise, professional answer citing specific clauses where possible.
            """
        else:
            prompt = f"""
            You are a legal analysis AI.
            Use the document and retrieved legal clauses below to perform a true legal analysis.

            DOCUMENT:
            {text[:8000]}

            RELEVANT CLAUSES:
            {context}

            Provide:
            - Key legal risks
            - Governing law detection
            - Compliance issues
            - Parties & obligations
            """

        try:
            response = self.model_pro.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def basic_summary(self, text: str) -> str:
        if not self.model_flash:
            return "Summarizer not configured."

        prompt = f"Summarize this non-legal document in 5 points:\n{text[:5000]}"
        
        try:
            response = self.model_flash.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"
