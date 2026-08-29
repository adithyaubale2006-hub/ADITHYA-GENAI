import os
from dotenv import load_dotenv
import google as genai

# Load the environment variables
load_dotenv()

# Configure the API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Test the connection
try:
    response = model.generate_content("Say hello!")
    print("\n✅ SUCCESS: API is working! Response from Gemini:", response.text)
except Exception as e:
    print("\n❌ ERROR: API failed to load. Details:", e)