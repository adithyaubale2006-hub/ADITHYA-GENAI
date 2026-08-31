import os
import re
import uuid
import certifi
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, Response, url_for
from google import genai
from google.genai import types

# Fix SSL certificate path for local environments
os.environ["SSL_CERT_FILE"] = certifi.where()

# Load environment variables from .env (GEMINI_API_KEY)
load_dotenv()

# Initialize Gemini Client
client = genai.Client()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["IMAGE_FOLDER"] = os.path.join("static", "images")
app.config["JSON_AS_ASCII"] = False

# Ensure required directories exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["IMAGE_FOLDER"], exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    return render_template("index1.html")


@app.route("/translate", methods=["POST"])
def translate_audio():
    language = request.form.get("language") or "English"
    file = request.files.get("file")

    if not file or not file.filename:
        return jsonify({"error": "No audio file provided."}), 400

    try:
        # Save audio file locally
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Upload file to Gemini Files API
        print(f"Uploading {file.filename} to Gemini...")
        audio_file = client.files.upload(file=file_path)

        print(f"Translating speech into {language}...")
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[audio_file],
            config=types.GenerateContentConfig(
                system_instruction=(
                    f"You are a strict translation engine. Translate all spoken speech in the audio directly into {language}. "
                    f"Return ONLY the plain translated text in {language}. "
                    "Do NOT include thought tags, markdown backticks, phonetic transcriptions, notes, or introductory words."
                ),
                temperature=0.2,
                max_output_tokens=2048,
            ),
        )

        raw_text = response.text or ""

        # Post-processing: remove thoughts, formatting, and unwanted artifacts
        clean_text = re.sub(r"<thought>.*?</thought>", "", raw_text, flags=re.DOTALL)
        clean_text = re.sub(r"```[a-zA-Z]*", "", clean_text)
        clean_text = clean_text.replace("```", "")
        clean_text = clean_text.replace("⏱️thought\n", "")
        clean_text = re.sub(r"^[-\s*+]+", "", clean_text)
        clean_text = clean_text.strip()

        return Response(clean_text, content_type="text/plain; charset=utf-8")

    except Exception as e:
        print(f"Error during translation: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/generate-image", methods=["POST"])
def generate_image():
    prompt = request.form.get("prompt")

    if not prompt:
        return jsonify({"error": "No prompt provided."}), 400

    try:
        print(f"Generating image for prompt: '{prompt}'")

        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )

        # Extract image bytes
        image_bytes = None
        if response.parts:
            for part in response.parts:
                if part.inline_data:
                    image_bytes = part.inline_data.data
                    break

        if not image_bytes:
            return jsonify({"error": "No image data returned from model."}), 500

        # Save generated image locally
        filename = f"generated_{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(app.config["IMAGE_FOLDER"], filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        image_url = url_for("static", filename=f"images/{filename}")
        return jsonify({"image_url": image_url})

    except Exception as e:
        print(f"Error during image generation: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)