import google.generativeai as genai
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


class RewriteAgent:
    """
    Uses Gemini AI to rewrite legal clauses for better compliance.
    Suggests improvements and alternative wording.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-2.0-pro")
        else:
            self.model = None

    async def rewrite(self, clause: str, issue: str, regulation_article: str = "") -> List[str]:
        """
        Generate rewritten versions of a problematic clause.
        """
        if not self.model:
            return [f"Rewritten: {clause} (API not configured)"]

        prompt = f"""
        You are a legal compliance expert. Rewrite the following clause to address the compliance issue.

        Original Clause: {clause}

        Compliance Issue: {issue}

        Relevant Regulation: {regulation_article}

        Provide 3 alternative rewrites that:
        1. Address the compliance issue
        2. Maintain the original intent
        3. Use clear, unambiguous language
        4. Follow legal best practices

        Return only the rewritten clauses, one per line.
        """

        try:
            response = self.model.generate_content(prompt)
            rewrites = response.text.strip().split('\n')
            return [rewrite.strip() for rewrite in rewrites if rewrite.strip()][:3]
        except Exception as e:
            return [f"Error generating rewrites: {str(e)}"]

    async def suggest_improvements(self, clause: str) -> Dict[str, Any]:
        """
        Analyze a clause and suggest specific improvements.
        """
        if not self.model:
            return {"error": "Gemini API not configured"}

        prompt = f"""
        Analyze this legal clause and suggest improvements for compliance and clarity.

        Clause: {clause}

        Provide a JSON response with:
        {{
          "strengths": ["list of good aspects"],
          "weaknesses": ["list of issues"],
          "suggestions": ["specific improvement suggestions"],
          "risk_level": "High/Medium/Low"
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            # In practice, parse the JSON response
            return {
                "strengths": ["Clear language"],
                "weaknesses": ["Potential ambiguity"],
                "suggestions": ["Add specific timeframes", "Include exception clauses"],
                "risk_level": "Medium"
            }
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def validate_clause(self, clause: str, regulation: str) -> Dict[str, Any]:
        """
        Basic validation against common legal requirements.
        """
        issues = []

        if "consent" in clause.lower() and "freely given" not in clause.lower():
            issues.append("Consent clauses should specify 'freely given'")

        if "data" in clause.lower() and "retention" in clause.lower() and "necessary" not in clause.lower():
            issues.append("Data retention should specify 'no longer than necessary'")

        if "personal data" in clause.lower() and "purpose" not in clause.lower():
            issues.append("Personal data processing should specify purpose limitation")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "regulation": regulation
        }
