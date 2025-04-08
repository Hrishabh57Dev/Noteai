from gtts import gTTS
import os

def text_to_speech(text, output_path="output.mp3", language="en", slow=False):
    """
    Converts text to speech and saves it as an audio file.

    Args:
        text (str): Input text to convert to speech.
        output_path (str): Path to save the audio file.
        language (str): Language code for the speech (e.g., "en" for English, "es" for Spanish).
        slow (bool): If True, the speech will be slower.

    Returns:
        str: Path to the saved audio file.
    """
    try:
        # Generate speech using gTTS
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(output_path)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to generate speech: {e}")
