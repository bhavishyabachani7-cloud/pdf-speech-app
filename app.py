from flask import Flask, render_template, request
import PyPDF2
import edge_tts
import asyncio
import uuid
import os

app = Flask(__name__)

os.makedirs("static", exist_ok=True)

VOICE_MAP = {
    "female_india": "en-IN-NeerjaNeural",
    "male_india": "en-IN-PrabhatNeural",
    "female_us": "en-US-JennyNeural",
    "male_uk": "en-GB-RyanNeural"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    mode = request.form.get("mode")
    voice = request.form.get("voice")
    speed = request.form.get("speed", "1")
    text = ""

    if mode == "pdf":
        file = request.files.get("pdf")
        if not file or file.filename == "":
            return "❌ Please upload a PDF file!"
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif mode == "text":
        text = request.form.get("text")
        if not text.strip():
            return "❌ Please enter some text!"
    if not text.strip():
        return "❌ No text found!"

    rate = "+0%"
    if speed == "0.8":
        rate = "-20%"
    elif speed == "1.2":
        rate = "+20%"
    elif speed == "1.5":
        rate = "+40%"

    voice_name = VOICE_MAP.get(voice, "en-IN-NeerjaNeural")
    filename = f"static/{uuid.uuid4()}.mp3"

    async def generate():
        communicate = edge_tts.Communicate(text, voice_name, rate=rate)
        await communicate.save(filename)

    asyncio.run(generate())

    return render_template("result.html", audio_file=filename)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
