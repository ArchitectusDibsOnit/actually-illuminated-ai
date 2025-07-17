# emotion_aware_tts.py
# Emotion-Aligned TTS Engine with Clippy & Bark Integration

import random
from bark_integration import generate_bark_audio
from phoneme_and_meta_tag_utils import get_tags
from voice_fx_chain import apply_voice_effects
import tempfile

# Basic emotion-to-tag mapping
emotion_tags = {
    "Happy": ["[cheerful]", "[bright]"],
    "Sad": ["[melancholy]", "[soft]"],
    "Angry": ["[intense]", "[distorted]"],
    "Surprise": ["[playful]", "[dynamic]"],
    "Fear": ["[whispering]", "[tense]"],
    "Disgust": ["[raspy]", "[gritty]"],
    "Neutral": ["[narrative-speaking]"],
}

def get_emotion_tags(emotion: str) -> str:
    tags = emotion_tags.get(emotion, ["[narrative-speaking]"])
    return " ".join(tags)

def synthesize_emotion_tts(text: str, emotion: str = "Neutral", speaker_id: str = "clippy") -> str:
    meta_tags = get_emotion_tags(emotion)
    prompt = f"{text} {meta_tags}"

    # Step 1: Generate raw audio from Bark
    raw_path = generate_bark_audio(prompt, speaker=speaker_id)

    # Step 2: Apply effects based on emotion (optional)
    fx_path = apply_voice_effects(raw_path, emotion)

    return fx_path

# For Clippy-style prompts
if __name__ == "__main__":
    sample = "Hey! Need help picking the right TTS voice?"
    path = synthesize_emotion_tts(sample, emotion="Happy")
    print(f"Audio ready: {path}")
