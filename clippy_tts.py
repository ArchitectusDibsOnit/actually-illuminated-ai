# clippy_tts.py (TTS With Emotion Matching)

import pyttsx3

# Mapping of emotion to voice parameters (basic)
EMOTION_VOICE_SETTINGS = {
    "Happy": {"rate": 180, "volume": 1.0},
    "Sad": {"rate": 120, "volume": 0.6},
    "Angry": {"rate": 190, "volume": 1.0},
    "Surprise": {"rate": 200, "volume": 0.9},
    "Fear": {"rate": 140, "volume": 0.7},
    "Disgust": {"rate": 100, "volume": 0.6},
    "Neutral": {"rate": 150, "volume": 0.8},
}

def speak_with_emotion(text, emotion="Neutral"):
    engine = pyttsx3.init()
    settings = EMOTION_VOICE_SETTINGS.get(emotion, EMOTION_VOICE_SETTINGS["Neutral"])

    engine.setProperty('rate', settings["rate"])
    engine.setProperty('volume', settings["volume"])

    voices = engine.getProperty('voices')
    # Optional: Select a preferred voice index if desired
    if voices:
        engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak_with_emotion("I am Clippy, here to help you emotionally.", "Happy")
