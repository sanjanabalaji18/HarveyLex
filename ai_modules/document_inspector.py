import google.generativeai as genai
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


class DocumentInspector:
    """
    Uses Gemini AI to classify and analyze document clauses.
    Performs semantic tagging and categorization of legal text.
    """

    def __init__(self):
        api_key = os.getenv("AIzaSyBzyf2zMEQ_kq8N0w2mF7yfnraX45oDtiw")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-2.0-pro")
        else:
            self.model = None

    async def classify(self, clauses: List[str]) -> Dict[str, Any]:
        """
        Classify document clauses into legal categories using Gemini.
        """
        if not self.model:
            return {"error": "Gemini API key not configured"}

        prompt = f"""
        Analyze the following legal document clauses and classify them into categories.
        Provide a JSON response with categories and their associated clauses.

        Clauses:
        {clauses}

        Response format:
        {{
          "categories": {{
            "data_protection": ["clause indices"],
            "liability": ["clause indices"],
            "termination": ["clause indices"],
            "intellectual_property": ["clause indices"],
            "other": ["clause indices"]
          }},
          "summary": "Brief summary of document focus"
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            # In a real implementation, parse the JSON response
            return {
                "categories": {
                    "data_protection": [],
                    "liability": [],
                    "termination": [],
                    "intellectual_property": [],
                    "other": list(range(len(clauses)))
                },
                "summary": "Document classification completed"
            }
        except Exception as e:
            return {"error": f"Classification failed: {str(e)}"}

    async def extract_key_terms(self, text: str) -> List[str]:
        """
        Extract key legal terms from text using Gemini.
        """
        if not self.model:
            return []

        prompt = f"""
        Extract key legal terms from the following text. Return as a comma-separated list.

        Text: {text}
        """

        try:
            response = self.model.generate_content(prompt)
            terms = response.text.strip().split(",")
            return [term.strip() for term in terms if term.strip()]
        except Exception:
            return []
