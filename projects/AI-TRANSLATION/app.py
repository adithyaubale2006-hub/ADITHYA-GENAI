from google import genai
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, render_template, Response
import certifi
import json

os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()

# Initialize the Gemini Client
# It automatically picks up GEMINI_API_KEY from your .env file
client = genai.Client()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static"
app.config['JSON_AS_ASCII'] = False

# Ensure the upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        language = request.form.get('language') 
        file = request.files.get('file') 

        # 1. DEBUG CHECK: Print the language to your VS Code terminal 
        # to ensure it actually says "Hindi" and isn't blank
        print(f"DEBUG - Target Language: '{language}'")

        if file and file.filename:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            print(f"Uploading {file.filename} to Gemini...")
            audio_file = client.files.upload(file=file_path) 

            print(f"Translating audio directly into {language}...")
            
            # 2. STRICTER PROMPT: Tell Gemini to ONLY output the target language
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[
                    audio_file,
                    f"Listen to the speech in this audio. Translate it directly into {language}. Return ONLY the final {language} translation. Do not include the original English transcription or any formatting." 
                ],
                config={
                    "temperature": 0.4, # Lowered the temperature slightly for more focused output
                    "max_output_tokens": 2048
                }
            )

            # ... Gemini generation code above ...
            
            clean_text = response.text.replace("⏱️thought\n", "").strip()

            # Force UTF-8 rendering using Python's native json module
            return Response(clean_text, content_type="text/plain; charset=utf-8")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)