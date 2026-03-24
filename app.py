from flask import Flask, render_template, request
import os
import uuid
import PyPDF2
import asyncio
import edge_tts

app = Flask(__name__)

if not os.path.exists("static"):
    os.makedirs("static")

VOICE_MAP = {
    "female_india": "en-IN-NeerjaNeural",
    "male_india": "en-IN-PrabhatNeural",
    "female_us": "en-US-JennyNeural",
    "male_uk": "en-GB-RyanNeural"
}

@app.route("/")
def index():
    return render_template("index.html")

async def generate_audio(text, voice, filename):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

@app.route("/convert", methods=["POST"])
def convert():
    text = ""
    mode = request.form.get("mode")
    voice_key = request.form.get("voice")

    voice = VOICE_MAP.get(voice_key, "en-IN-NeerjaNeural")

    if mode == "pdf":
        pdf_file = request.files["pdf"]
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() or ""

    elif mode == "text":
        text = request.form.get("text")

    if not text.strip():
        return "No text found!"

    filename = f"static/{uuid.uuid4()}.mp3"

    # 🔥 FIX: Safe async run
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(generate_audio(text, voice, filename))
    loop.close()

    return render_template("result.html", audio_file=filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
