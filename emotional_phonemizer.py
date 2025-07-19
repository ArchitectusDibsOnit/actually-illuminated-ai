# emotional_phonemizer.py (Updated to use meta_tag_manager)

import re
from meta_tag_manager import detect_tags

# Simulated phoneme and emotion mappings
EMOTION_KEYWORDS = {
    "happy": ["joy", "glad", "cheerful"],
    "sad": ["sorrow", "down", "blue"],
    "angry": ["mad", "furious", "rage"],
    "calm": ["peace", "relaxed", "serene"],
}

PHONEME_DICT = {
    "hello": "HH AH0 L OW1",
    "world": "W ER1 L D",
    "joy": "JH OY1",
    "sorrow": "S AO1 R OW0",
    # ... more as needed
}

GLYPH_ANIMATIONS = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "calm": "😌",
    # fallback glyph
    "neutral": "😐",
}

def analyze_text_for_phonemes_and_emotion(text):
    words = re.findall(r"\w+", text.lower())
    phonemes = []
    emotion_score = {k: 0 for k in EMOTION_KEYWORDS}

    for word in words:
        ph = PHONEME_DICT.get(word, "")
        if ph:
            phonemes.append(ph)

        for emo, keywords in EMOTION_KEYWORDS.items():
            if word in keywords:
                emotion_score[emo] += 1

    dominant_emotion = max(emotion_score, key=emotion_score.get)
    dominant_glyph = GLYPH_ANIMATIONS.get(dominant_emotion, GLYPH_ANIMATIONS["neutral"])
    detected_tags = detect_tags(text)

    return {
        "phonemes": " ".join(phonemes),
        "emotion": dominant_emotion,
        "glyph": dominant_glyph,
        "tags": detected_tags
    }
