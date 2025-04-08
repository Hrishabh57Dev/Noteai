import os

def create_directories():
    """
    Creates necessary directories for the project.
    """
    directories = [
        "../storage/audio_files",       # For storing uploaded audio files
        "../storage/output",            # For storing exported JSON/CSV files
        "../storage/pdfs",              # For storing generated PDF files
        "../models/whisper_model",      # For storing Whisper ASR models
        "../models/summarization_model" # For storing summarization models
    ]

    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Directory '{directory}' is ready.")
        except Exception as e:
            print(f"Error creating directory '{directory}': {e}")

if __name__ == "__main__":
    create_directories()
