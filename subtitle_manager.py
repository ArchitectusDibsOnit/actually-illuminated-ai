# subtitle_manager.py

import os
import whisper

whisper_model = whisper.load_model("base")

SUBTITLE_DIR = "subtitles"
os.makedirs(SUBTITLE_DIR, exist_ok=True)

def transcribe_audio(audio_path):
    result = whisper_model.transcribe(audio_path)
    return result["text"], result["segments"]

def save_subtitles(text, audio_filename):
    base_name = os.path.splitext(audio_filename)[0]
    subtitle_path = os.path.join(SUBTITLE_DIR, f"{base_name}_subtitles.txt")
    with open(subtitle_path, "w") as f:
        f.write(text)

def get_subtitles(audio_filename):
    base_name = os.path.splitext(audio_filename)[0]
    subtitle_path = os.path.join(SUBTITLE_DIR, f"{base_name}_subtitles.txt")
    if os.path.exists(subtitle_path):
        with open(subtitle_path, "r") as f:
            return f.read()
    return ""

def auto_generate_phonemes(text, text_to_phonemes_func):
    return text_to_phonemes_func(text)
