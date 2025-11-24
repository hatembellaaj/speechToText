from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os
import subprocess

app = Flask(__name__)
CORS(app)

model = whisper.load_model("small")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        audio_file = request.files["audio"]
        audio_path = "temp_audio_input"
        os.makedirs(audio_path, exist_ok=True)

        file_path = os.path.join(audio_path, audio_file.filename)
        audio_file.save(file_path)

        # 🔍 Vérifie que le fichier contient bien du son
        try:
            duration_cmd = [
                "ffprobe", "-i", file_path, "-show_entries", "format=duration",
                "-v", "quiet", "-of", "csv=p=0"
            ]
            duration = float(subprocess.check_output(duration_cmd).decode().strip())
            if duration < 0.1:
                return jsonify({"text": "Erreur : fichier audio vide ou très court"}), 400
        except Exception:
            pass  # ignore si ffprobe indisponible

        # 🎙️ Transcription
        result = model.transcribe(file_path, language="fr")
        return jsonify({"text": result["text"]})

    except Exception as e:
        print("Erreur :", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5020, debug=False)

