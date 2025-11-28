import google.generativeai as genai
import os
from backend.datastore.pdf_reader import PDFReader


class DocumentInspector:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    def analyze_text(self, text: str, query: str):
        prompt = f"""
You are a compliance expert. Analyze the following text based on the query.

Query: {query}

Text:
{text}

Provide a short, accurate analysis.
"""
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
