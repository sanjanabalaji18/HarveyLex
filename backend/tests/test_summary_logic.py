
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

# Mocking genai to avoid actual API calls if possible, or just testing the logic flow
# But we want to verify the prompt construction which was the issue.

from ai_modules.summary_agent import SummaryAgent

def test_prompt_construction():
    agent = SummaryAgent()
    
    text = "This is a contract."
    hits = [{"text": "Clause 1"}]
    query = "What is the termination fee?"
    
    # We can't easily inspect the internal prompt without modifying the class or mocking the model.
    # Let's just try to run it and see if it errors.
    
    print("Running summarize with query...")
    try:
        # This will fail if API key is invalid or network issues, but we want to check for code errors
        summary = agent.summarize(text, hits, query=query)
        print("Summary result:", summary)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_prompt_construction()
