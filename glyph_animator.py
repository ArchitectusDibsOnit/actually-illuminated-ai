# glyph_animator.py (Handles PNG/GIF switching by emotion)

import os
from PIL import Image
import shutil

ASSETS_DIR = "assets"
ACTIVE_PATH = os.path.join(ASSETS_DIR, "glyphclippy_idle.png")

emotion_to_asset = {
    "Joy": "glyphclippy_happy.gif",
    "Anger": "glyphclippy_angry.gif",
    "Sadness": "glyphclippy_sad.gif",
    "Optimism": "glyphclippy_thinking.gif",
    "Neutral": "glyphclippy_idle.png"
}

class GlyphAnimator:
    def set_emotion(self, emotion):
        filename = emotion_to_asset.get(emotion, "glyphclippy_idle.png")
        full_path = os.path.join(ASSETS_DIR, filename)
        if os.path.exists(full_path):
            try:
                shutil.copy(full_path, ACTIVE_PATH)
                print(f"[🎞️] Clippy switched to {emotion} mode: {filename}")
            except Exception as e:
                print(f"[⚠️] Error switching animation: {e}")
