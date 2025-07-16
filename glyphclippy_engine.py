# glyphclippy_engine.py (Stateful Emotion-Synced Clippy)

import os

class GlyphClippy:
    _memory = []
    _state = "idle"  # idle, thinking, talking, etc.

    _emotion_state_map = {
        "idle": "assets/clippy_states/glyphclippy_idle.png",
        "thinking": "assets/clippy_states/glyphclippy_thinking.gif",
        "talking": "assets/clippy_states/glyphclippy_talking.gif",
        "smile": "assets/clippy_states/glyphclippy_smile.gif",
        "rage": "assets/clippy_states/glyphclippy_rage.gif",
        "jump": "assets/clippy_states/glyphclippy_surprise.gif",
        "shiver": "assets/clippy_states/glyphclippy_fear.gif",
        "gag": "assets/clippy_states/glyphclippy_disgust.gif",
        "droop": "assets/clippy_states/glyphclippy_sad.gif",
    }

    @classmethod
    def chat(cls, message):
        cls._memory.append(message)
        cls.set_state("talking")
        return f"Clippy says: '{message[::-1]}' (fake response)"

    @classmethod
    def get_memory(cls):
        return "\n".join(cls._memory[-5:])

    @classmethod
    def clear_memory(cls):
        cls._memory.clear()
        cls.set_state("idle")

    @classmethod
    def set_state(cls, state):
        if state in cls._emotion_state_map:
            cls._state = state
        else:
            cls._state = "idle"

    @classmethod
    def get_image(cls):
        return cls._emotion_state_map.get(cls._state, cls._emotion_state_map["idle"])

# Export for external control
set_clippy_state = GlyphClippy.set_state
get_clippy_image = GlyphClippy.get_image
