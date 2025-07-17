# subtitle_ui.py

import os
import json
import tkinter as tk
from tkinter import ttk
from clippy_voice_engine import speak
from emotional_phonemizer import text_to_phonemes
from emotion_engine import detect_emotion

class SubtitleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GlyphClippy Subtitle Interface")

        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.subtitle_text = tk.StringVar()
        self.emotion_label = tk.StringVar(value="Emotion: Neutral")
        self.voice_feedback = tk.StringVar(value="TTS: Ready")

        self._build_widgets()

    def _build_widgets(self):
        ttk.Label(self.frame, text="Enter Subtitle:").grid(row=0, column=0, sticky=tk.W)
        entry = ttk.Entry(self.frame, textvariable=self.subtitle_text, width=60)
        entry.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))
        entry.bind('<Return>', self.process_subtitle)

        ttk.Button(self.frame, text="Speak", command=self.process_subtitle).grid(row=2, column=0, sticky=tk.W)
        ttk.Label(self.frame, textvariable=self.emotion_label).grid(row=2, column=1, sticky=tk.W)
        ttk.Label(self.frame, textvariable=self.voice_feedback).grid(row=2, column=2, sticky=tk.E)

    def process_subtitle(self, *args):
        subtitle = self.subtitle_text.get().strip()
        if not subtitle:
            self.voice_feedback.set("TTS: No input provided.")
            return

        emotion = detect_emotion(subtitle)
        phonemes = text_to_phonemes(subtitle)

        self.emotion_label.set(f"Emotion: {emotion.capitalize()}")
        result = speak(subtitle, emotion=emotion)
        self.voice_feedback.set(result)


if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleUI(root)
    root.mainloop()
