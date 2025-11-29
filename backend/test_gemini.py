import os
import google.generativeai as genai
from dotenv import load_dotenv
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("API call timed out after 10 seconds")

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(10)  # 10 second timeout
    
    model = genai.GenerativeModel('gemini-pro')  # Using gemini-pro instead
    response = model.generate_content("Hello")
    
    signal.alarm(0)  # Cancel the alarm
    print("✅ Success!")
    print(f"Response: {response.text}")
except TimeoutError as e:
    print(f"❌ Timeout: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
