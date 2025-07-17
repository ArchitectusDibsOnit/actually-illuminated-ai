# glyphclippy_engine.py (Emotion + TTS + Animation + Memory Core)

import random
import json
import os
from tts_pipeline import speak_text_with_emotion
from glyph_animator import GlyphAnimator

GLYPHCLIPPY_MEMORY_FILE = "glyphclippy_memory.json"

class GlyphClippyEngine:
    def __init__(self):
        self.memory = []
        self.animator = GlyphAnimator()
        if os.path.exists(GLYPHCLIPPY_MEMORY_FILE):
            with open(GLYPHCLIPPY_MEMORY_FILE, 'r') as f:
                self.memory = json.load(f)

    def chat(self, message):
        reply = self._generate_response(message)
        emotion = self._detect_emotion(reply)
        self.animator.set_emotion(emotion)
        speak_text_with_emotion(reply, emotion)
        self.memory.append({"user": message, "clippy": reply, "emotion": emotion})
        self._save_memory()
        return reply

    def get_memory(self):
        return json.dumps(self.memory[-5:], indent=2)

    def clear_memory(self):
        self.memory = []
        self._save_memory()

    def _save_memory(self):
        with open(GLYPHCLIPPY_MEMORY_FILE, 'w') as f:
            json.dump(self.memory, f)

    def _generate_response(self, message):
        # Simple stubbed logic; can be replaced with GPT or local model
        responses = [
            "Sure thing! Let me help you with that.",
            "Absolutely! Here's what I found...",
            "Give me a second... Scanning neural archives...",
            "Of course! This one’s interesting..."
        ]
        return random.choice(responses)

    def _detect_emotion(self, text):
        from emotion_detector import detect_emotion
        return detect_emotion(text)

GlyphClippy = GlyphClippyEngine()
