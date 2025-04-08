from flask import Flask, request, jsonify, Response, send_from_directory
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from flask_cors import CORS
import logging
from backend.celery_config import celery_app
from backend.transcriber import transcribe_audio, process_youtube_video
from backend.summarizer import summarize_text
from backend.pdf_parser import extract_text_from_pdf
from backend.keyword_extractor import extract_keywords
from backend.tts import text_to_speech
from backend.database import init_db, save_note, get_notes
import os

# Initialize Flask app
app = Flask(
    __name__,
    static_folder="../frontend",  # Serve static files from the frontend directory
    static_url_path="/"          # Serve static files at the root URL
)

# Serve the index.html file
@app.route("/")
def serve_index():
    """Serve the main frontend page."""
    return send_from_directory(app.static_folder, "index.html")

# Serve static files (e.g., CSS, JS)
@app.route("/<path:filename>")
def serve_static_files(filename):
    """Serve static files like CSS and JS."""
    return send_from_directory(app.static_folder, filename)

# Metrics endpoint
@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics"""
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

# Health check endpoint
@app.route('/health')
def health_check():
    """Service health check"""
    return {'status': 'healthy'}, 200
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize database
init_db()

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Save the uploaded file
        audio_dir = "../storage/audio_files"
        os.makedirs(audio_dir, exist_ok=True)
        file_path = os.path.join(audio_dir, file.filename)
        file.save(file_path)

        # Transcribe the file
        transcription = transcribe_audio(file_path)
        return jsonify({"transcription": transcription})
    except Exception as e:
        logging.error(f"Error in /transcribe: {e}")
        return jsonify({"error": "Failed to transcribe audio"}), 500

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.json
        transcription = data.get("transcription")
        if not transcription:
            return jsonify({"error": "No transcription provided"}), 400

        # Summarize the transcription
        summary = summarize_text(transcription)
        return jsonify({"summary": summary})
    except Exception as e:
        logging.error(f"Error in /summarize: {e}")
        return jsonify({"error": "Failed to summarize text"}), 500

@app.route("/extract_pdf", methods=["POST"])
def extract_pdf():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Save the uploaded PDF
        pdf_dir = "../storage/pdf_files"
        os.makedirs(pdf_dir, exist_ok=True)
        file_path = os.path.join(pdf_dir, file.filename)
        file.save(file_path)

        # Extract text from the PDF
        text = extract_text_from_pdf(file_path)
        return jsonify({"text": text})
    except Exception as e:
        logging.error(f"Error in /extract_pdf: {e}")
        return jsonify({"error": "Failed to extract text from PDF"}), 500

@app.route("/extract_keywords", methods=["POST"])
def extract_keywords_api():
    try:
        data = request.json
        text = data.get("text")
        method = data.get("method", "spacy")
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Extract keywords
        keywords = extract_keywords(text, method)
        return jsonify({"keywords": keywords})
    except Exception as e:
        logging.error(f"Error in /extract_keywords: {e}")
        return jsonify({"error": "Failed to extract keywords"}), 500

@app.route("/text_to_speech", methods=["POST"])
def text_to_speech_api():
    try:
        data = request.json
        text = data.get("text")
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Convert text to speech
        audio_dir = "../storage/audio_files"
        os.makedirs(audio_dir, exist_ok=True)
        output_path = os.path.join(audio_dir, "output.mp3")
        audio_path = text_to_speech(text, output_path)
        return jsonify({"audio_path": audio_path})
    except Exception as e:
        logging.error(f"Error in /text_to_speech: {e}")
        return jsonify({"error": "Failed to convert text to speech"}), 500

@app.route("/notes", methods=["GET", "POST"])
def notes():
    try:
        if request.method == "POST":
            data = request.json
            title = data.get("title")
            transcription = data.get("transcription")
            summary = data.get("summary")
            quiz = data.get("quiz")
            if not title or not transcription or not summary or not quiz:
                return jsonify({"error": "Missing note data"}), 400

            # Save note to database
            save_note(title, transcription, summary, quiz)
            return jsonify({"message": "Note saved successfully"}), 201

        elif request.method == "GET":
            # Retrieve notes from database
            notes = get_notes()
            return jsonify({"notes": notes})
    except Exception as e:
        logging.error(f"Error in /notes: {e}")
        return jsonify({"error": "Failed to process notes"}), 500

@app.route("/process_youtube", methods=["POST"])
def process_youtube():
    """
    Processes a YouTube video by downloading its audio, transcribing it, and summarizing the transcription.
    """
    try:
        data = request.json
        youtube_url = data.get("youtube_url")
        method = data.get("method", "abstractive")
        length = data.get("length", "medium")

        if not youtube_url:
            return jsonify({"error": "YouTube URL is required"}), 400

        # Transcribe the YouTube video
        transcription = process_youtube_video(youtube_url)

        # Summarize the transcription
        summary = summarize_text(transcription, method, length)

        return jsonify({"transcription": transcription, "summary": summary})
    except Exception as e:
        logging.error(f"Error in /process_youtube: {e}")
        return jsonify({"error": "Failed to process YouTube video"}), 500

if __name__ == "__main__":
    app.run(debug=True)