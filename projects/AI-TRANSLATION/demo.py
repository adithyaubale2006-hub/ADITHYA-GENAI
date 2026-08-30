import os
import certifi
from dotenv import load_dotenv
from google import genai

# FIX: Force Python to use the certifi certificate bundle for secure connections
os.environ["SSL_CERT_FILE"] = certifi.where()

# Load environment variables
load_dotenv()

# Initialize the Gemini client
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

# Upload the mp3 file using the client
print("Uploading file...")
audio_file = client.files.upload(file=r"C:\Users\ADITHYA UBALE\OneDrive\Desktop\AUDIO-TRANSLATION\harvard.mp3") 
print(f"Uploaded file '{audio_file.display_name}' as: {audio_file.name}")

# Initialize the model and generate content
print("Generating transcript...")
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=[
        "Please transcribe this audio and translate it into English.", 
        audio_file
    ]
)

# Print the result
print(response.text)