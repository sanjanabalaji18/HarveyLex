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
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    def summarize(self, text: str, context_results: List[Dict[str, Any]]) -> str:
        if not self.model:
            return "Summarizer not configured."

        context_str = "\n".join([f"- {item.get('text', '')}" for item in context_results])
        
        prompt = f"""
        You are a legal assistant. Summarize the following document text, taking into account the relevant regulations provided.

        Document Text:
        {text[:5000]}

        Relevant Regulations:
        {context_str}

        Provide a comprehensive summary highlighting compliance status and key legal points.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def basic_summary(self, text: str) -> str:
        if not self.model:
            return "Summarizer not configured."

        prompt = f"""
        Summarize the following text:

        Text:
        {text[:5000]}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"
