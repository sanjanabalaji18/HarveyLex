
import os
from dotenv import load_dotenv

# Load environment variables
# load_dotenv() will search for .env in current and parent directories by default
found = load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print(f"Dotenv found: {found}")
if api_key:
    masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "***"
    print(f"GEMINI_API_KEY is SET. (Value starts with: {masked_key[:4]})")
else:
    print("GEMINI_API_KEY is NOT SET.")
