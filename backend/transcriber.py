import whisper
import os

def transcribe_audio(file_path, language=None):
    """
    Transcribes the given audio file to text using Whisper.

    Args:
        file_path (str): Path to the audio file.
        language (str, optional): Language code for transcription (e.g., "en" for English).
                                  If None, Whisper will auto-detect the language.

    Returns:
        str: The transcribed text.
    """
    # Load the Whisper model
    model = whisper.load_model("base")

    # Preprocess the audio file (e.g., noise reduction can be added here if needed)
    # Whisper handles most preprocessing internally.

    # Transcribe the audio file
    options = {"language": language, "task": "transcribe"} if language else {"task": "transcribe"}
    result = model.transcribe(file_path, **options)

    # Extract and format the transcription
    transcription = result.get("text", "").strip()

    return transcription