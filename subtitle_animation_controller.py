# subtitle_animation_controller.py

import time
import threading
from subtitle_emotion_manager import SubtitleEmotionTracker
from clippy_speaker import ClippySpeechSynth

class SubtitleAnimator:
    def __init__(self):
        self.tracker = SubtitleEmotionTracker()
        self.speaker = ClippySpeechSynth()
        self.running = False
        self.active_emotion = "neutral"
        self.current_glyph = "😐"
        self.callback = None

    def bind_subtitles(self, subtitle_lines):
        """
        Accepts a list of subtitle dicts with start/end/text and processes them.
        """
        self.tracker.process_subtitles(subtitle_lines)

    def start_animation_loop(self, on_emotion_change_callback=None):
        """
        Begins a thread that constantly checks the current emotion and updates UI.
        """
        self.running = True
        self.callback = on_emotion_change_callback

        def loop():
            start_time = time.time()
            while self.running:
                elapsed = time.time() - start_time
                emotion, glyph = self.tracker.get_current_emotion(elapsed)
                if glyph and emotion != self.active_emotion:
                    self.active_emotion = emotion
                    self.current_glyph = glyph
                    print(f"[!] Emotion changed to: {emotion} {glyph}")
                    if self.callback:
                        self.callback(emotion, glyph)
                    self.speaker.speak_emotion(emotion)
                time.sleep(0.2)

        threading.Thread(target=loop, daemon=True).start()

    def stop_animation(self):
        self.running = False

    def get_current_state(self):
        return self.active_emotion, self.current_glyph
