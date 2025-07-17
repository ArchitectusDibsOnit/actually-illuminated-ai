# emotional_phonemizer.py

import re
import random

# Glyphs mapped to simplified emotion buckets
GLYPH_ANIMATIONS = {
    "neutral": "😐",
    "happy": "😄",
    "angry": "😠",
    "sad": "😢",
    "surprised": "😲",
    "excited": "🤩",
    "calm": "😌",
    "confused": "😕",
    "scared": "😱",
    "loving": "😍",
}

# Mock emotion lexicon (can be replaced with ML model or API call)
EMOTION_LEXICON = {
    "love": "loving",
    "hate": "angry",
    "joy": "happy",
    "happy": "happy",
    "sad": "sad",
    "cry": "sad",
    "angry": "angry",
    "fear": "scared",
    "wow": "surprised",
    "yay": "excited",
    "calm": "calm",
    "peace": "calm",
    "confused": "confused",
}

META_TAGS = [
    "#epic", "#lofi", "#trap", "#rock", "#pop", "#metal", "#emotional", "#cinematic", "#dark", "#uplifting",
    "#synthwave", "#dystopian", "#dreamy", "#orchestral", "#ambient", "#spokenword"
]

def detect_emotion(text):
    words = re.findall(r"\w+", text.lower())
    emotions = [EMOTION_LEXICON.get(word) for word in words if word in EMOTION_LEXICON]
    return emotions[0] if emotions else "neutral"

def generate_phonemes(text):
    return "-".join(list(text.lower()))

def detect_tags(text):
    tags_found = [tag for tag in META_TAGS if tag[1:] in text.lower() or tag in text.lower()]
    return tags_found

def analyze_text_for_phonemes_and_emotion(text):
    emotion = detect_emotion(text)
    phonemes = generate_phonemes(text)
    tags = detect_tags(text)
    return {
        "emotion": emotion,
        "glyph": GLYPH_ANIMATIONS.get(emotion, "😐"),
        "phonemes": phonemes,
        "tags": tags
    }

if __name__ == "__main__":
    sample = "I feel so much joy and peace in this moment. #ambient"
    enriched = analyze_text_for_phonemes_and_emotion(sample)
    print(enriched)
