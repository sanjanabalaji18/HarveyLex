import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

LEGAL_LABELS = ["contract", "agreement", "policy", "disclosure", "legal memo", "regulation"]
NON_LEGAL_LABELS = ["academic", "notes", "technical", "marketing", "other"]

class DocumentClassifier:
    def __init__(self):
        # Use the project's standard environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            # Fallback or error logging could go here
            print("Warning: GEMINI_API_KEY not found.")
        else:
            genai.configure(api_key=api_key)
            
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def classify_document(self, text: str) -> str:
        prompt = f"""
        Classify the following text into one of the categories:
        {LEGAL_LABELS + NON_LEGAL_LABELS}

        Return ONLY the category name.

        Text:
        {text[:2000]}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error: {str(e)}"
