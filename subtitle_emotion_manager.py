# subtitle_emotion_manager.py

import time
from emotional_phonemizer import analyze_text_for_phonemes_and_emotion

class SubtitleEmotionTracker:
    def __init__(self):
        self.timeline = []
        self.last_emotion = "neutral"

    def process_subtitles(self, subtitles):
        """
        Processes a list of subtitle lines into a phoneme + emotion timeline.
        Each line should be a dict with 'start', 'end', and 'text'.
        """
        for line in subtitles:
            result = analyze_text_for_phonemes_and_emotion(line['text'])
            entry = {
                "start": line['start'],
                "end": line['end'],
                "text": line['text'],
                "phonemes": result['phonemes'],
                "emotion": result['emotion'],
                "glyph": result['glyph'],
                "tags": result['tags']
            }
            self.timeline.append(entry)

    def get_current_emotion(self, current_time):
        """
        Returns the current active emotion + glyph based on the subtitle timeline.
        """
        for entry in self.timeline:
            if entry["start"] <= current_time <= entry["end"]:
                if entry["emotion"] != self.last_emotion:
                    self.last_emotion = entry["emotion"]
                    return entry["emotion"], entry["glyph"]
        return self.last_emotion, None  # No change

    def dump_timeline(self):
        return self.timeline
