# NotesAI Project

NotesAI is an AI-powered tool for converting audio/video files into transcriptions, summaries, quizzes, and downloadable PDFs. It includes a user-friendly web interface and supports advanced AI models for transcription and summarization.

## Project Structure
- **backend/**: Contains backend scripts for processing data.
- **frontend/**: Handles the user interface.
- **models/**: Stores AI models for transcription and summarization.
- **storage/**: Holds user-generated content like notes and recordings.
- **requirements.txt**: Lists project dependencies.
- **run.py**: Launches the backend server.
- **run.sh**: Shell script to automate setup and execution.

## Prerequisites
1. **Python**: Ensure Python 3.8 or higher is installed.
2. **Redis**: Install Redis for task management.
   - **Ubuntu/Debian**: `sudo apt install redis`
   - **macOS**: `brew install redis`
   - **Windows**: Download and install from [Redis for Windows](https://github.com/microsoftarchive/redis/releases).
3. **Tesseract OCR**: Install Tesseract for OCR functionality.
   - **Ubuntu/Debian**: `sudo apt install tesseract-ocr`
   - **macOS**: `brew install tesseract`
   - **Windows**: Download and install from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract).
4. **Poppler**: Install Poppler for PDF image conversion.
   - **Ubuntu/Debian**: `sudo apt install poppler-utils`
   - **macOS**: `brew install poppler`
   - **Windows**: Download and install from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/).
5. **FFmpeg**: Install FFmpeg for audio processing.
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download and install from [FFmpeg](https://ffmpeg.org/download.html).

## Environment Variables
Create a `.env` file in the root directory to configure environment variables:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
PORT=5000
```

## How to Run
1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```

2. **Set Up Directories**:
   ```bash
   python3 setup_directories.py
   ```

3. **Start Redis Server**:
   ```bash
   redis-server --daemonize yes
   ```

4. **Start Celery Worker**:
   ```bash
   celery -A backend.celery_config.celery_app worker --loglevel=info --hostname=worker1@%h
   ```

5. **Run the Application**:
   - Using the Python script:
     ```bash
     python3 run.py
     ```
   - Using the shell script:
     ```bash
     chmod +x run.sh
     ./run.sh
     ```

## Features
- **Transcription**: Convert audio/video files into text using OpenAI's Whisper.
- **Summarization**: Generate concise summaries using Hugging Face transformers or Sumy.
- **Keyword Extraction**: Extract key phrases using spaCy, YAKE, or TF-IDF.
- **PDF Parsing**: Extract text from text-based and scanned PDFs.
- **Text-to-Speech**: Convert text into speech using gTTS.
- **Notes Management**: Save, edit, delete, and search notes in a database.
- **Dark Mode**: Toggle between light and dark themes in the frontend.
- **Redis Caching**: Cache frequently used data for faster access.

## Troubleshooting
1. **Redis Not Found**:
   - Ensure Redis is installed and running:
     ```bash
     redis-server --daemonize yes
     redis-cli ping
     ```
2. **Tesseract Not Found**:
   - Ensure Tesseract is installed and its path is configured:
     ```python
     from pytesseract import pytesseract
     pytesseract.tesseract_cmd = r"/path/to/tesseract"
     ```
3. **Flask Not Found**:
   - Ensure Flask is installed and accessible:
     ```bash
     pip install flask
     flask --version
     ```
4. **Dependency Issues**:
   - Reinstall dependencies:
     ```bash
     pip install -r requirements.txt --break-system-packages
     ```

## Notes
- For development, use the `run.py` or `run.sh` scripts to automate setup and execution.
- Ensure all system-level dependencies are installed before running the application.
- Use the `.env` file to configure environment variables for Redis and Flask.
