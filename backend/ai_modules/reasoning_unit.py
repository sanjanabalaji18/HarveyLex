import google.generativeai as genai
from backend.core.logger import get_logger


class ReasoningUnit:
    async def evaluate_clause(self, clause, references):
        prompt = f"""
        You are a legal compliance review agent.

        Clause:
        {clause}

        Relevant legal references:
        {references}

        Produce a structured JSON:
        {{
          "compliance_rating": "High/Medium/Low",
          "conflicts_found": [],
          "justification": "",
          "recommended_fix": ""
        }}
        """

        model = genai.GenerativeModel("gemini-2.0-pro")
        response = model.generate_content(prompt)

        return response.text
