# clippy_voice_engine.py

import os
import json
import requests
import torch
import tempfile
from playsound import playsound

# Load TTS config
CONFIG_FILE = "tts_config.json"
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE) as f:
        config = json.load(f)
else:
    config = {
        "default_voice": "eleven_monotone_clippy",
        "tts_backend": "elevenlabs",
        "emotion_presets": {
            "neutral": {"stability": 0.5, "similarity_boost": 0.7},
            "happy": {"stability": 0.2, "similarity_boost": 0.9},
            "angry": {"stability": 0.8, "similarity_boost": 0.6},
            "sad": {"stability": 0.9, "similarity_boost": 0.4}
        }
    }

DEFAULT_VOICE = config.get("default_voice", "eleven_monotone_clippy")
TTS_BACKEND = config.get("tts_backend", "elevenlabs")
EMOTION_PRESETS = config.get("emotion_presets", {})

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "sk_8b1d94f8992d69cc3c8b78998ed6127984f24ee695df3270")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"


def is_gpu_available():
    return torch.cuda.is_available()


def speak(text, emotion="neutral", voice=DEFAULT_VOICE, backend=TTS_BACKEND):
    if backend == "elevenlabs":
        return speak_with_elevenlabs(text, voice, emotion)
    elif backend == "bark" and is_gpu_available():
        return speak_with_bark(text)
    elif backend == "tortoise" and is_gpu_available():
        return speak_with_tortoise(text)
    else:
        return f"TTS backend '{backend}' is unsupported or requires GPU."


def speak_with_elevenlabs(text, voice, emotion):
    settings = EMOTION_PRESETS.get(emotion.lower(), EMOTION_PRESETS.get("neutral"))
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": settings
    }
    try:
        response = requests.post(f"{ELEVENLABS_API_URL}/{voice}", json=payload, headers=headers)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(response.content)
            temp_audio_path = f.name
        playsound(temp_audio_path)
        os.remove(temp_audio_path)
        return "Spoken with ElevenLabs."
    except Exception as e:
        return f"Error using ElevenLabs TTS: {e}"


def speak_with_bark(text):
    try:
        from bark import SAMPLE_RATE, preload_models, generate_audio
        import soundfile as sf

        preload_models()
        audio_array = generate_audio(text)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            sf.write(f.name, audio_array, SAMPLE_RATE)
            playsound(f.name)
            os.remove(f.name)
        return "Spoken with Bark."
    except Exception as e:
        return f"Bark TTS failed: {e}"


def speak_with_tortoise(text):
    try:
        from tortoise.api import TextToSpeech
        from tortoise.utils.audio import load_audio, save_wav

        tts = TextToSpeech()
        gen = tts.tts(text, voice="daniel")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            save_wav(gen.squeeze(0), f.name)
            playsound(f.name)
            os.remove(f.name)
        return "Spoken with Tortoise."
    except Exception as e:
        return f"Tortoise TTS failed: {e}"


if __name__ == "__main__":
    print(speak("Hello, I'm Clippy and I'm here to help you make music!", emotion="happy"))
