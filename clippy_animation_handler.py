# clippy_animation_handler.py

import os
from PIL import Image
from itertools import cycle

class ClippyAnimator:
    def __init__(self, idle_path="assets/glyphclippy_idle.png", emotion_gif_dir="assets/emotions"):
        self.idle_path = idle_path
        self.emotion_gif_dir = emotion_gif_dir
        self.emotion_states = {}
        self._load_emotion_gifs()
        self.current_state = "Idle"
        self.current_animation = self.emotion_states.get("Idle", [Image.open(idle_path)])
        self.frame_cycle = cycle(self.current_animation)

    def _load_emotion_gifs(self):
        for fname in os.listdir(self.emotion_gif_dir):
            if fname.endswith(".gif"):
                state = fname.split(".")[0].capitalize()
                path = os.path.join(self.emotion_gif_dir, fname)
                try:
                    gif = Image.open(path)
                    frames = []
                    while True:
                        frames.append(gif.copy())
                        gif.seek(gif.tell() + 1)
                except EOFError:
                    pass
                self.emotion_states[state] = frames

    def set_emotion(self, emotion):
        emotion = emotion.capitalize()
        if emotion in self.emotion_states:
            self.current_state = emotion
            self.current_animation = self.emotion_states[emotion]
            self.frame_cycle = cycle(self.current_animation)
        else:
            self.current_state = "Idle"
            self.current_animation = [Image.open(self.idle_path)]
            self.frame_cycle = cycle(self.current_animation)

    def get_next_frame(self):
        return next(self.frame_cycle)


# Example usage (to be used with async UI update or frame refresh):
# clippy = ClippyAnimator()
# clippy.set_emotion("Happy")
# next_frame = clippy.get_next_frame()
