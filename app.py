from flask import Flask, render_template, request
import os
import PyPDF2
import uuid
from gtts import gTTS

app = Flask(__name__)

# Ensure static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    mode = request.form.get('mode')
    voice = request.form.get('voice')
    text = ""

    try:
        # 📄 PDF → Speech
        if mode == "pdf":
            pdf_file = request.files['pdf']
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text() or ""

        # ✍️ Text → Speech
        elif mode == "text":
            text = request.form.get('text')

        if not text.strip():
            return "❌ No text found."

        # 🎙️ Voice styles
        if voice == "calm":
            slow = True
            tld = "co.in"
        elif voice == "fast":
            slow = False
            tld = "com"
        else:
            slow = False
            tld = "co.in"

        # 🎧 Generate audio
        filename = f"static/{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang='en', tld=tld, slow=slow)
        tts.save(filename)

        return render_template('result.html', audio_file=filename)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run()
