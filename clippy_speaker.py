# clippy_speaker.py

import pyttsx3

class ClippySpeechSynth:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")

        # Voice tuning (platform-dependent, may need adjustment)
        self.voice_profiles = {
            "happy": {"rate": 180, "voice_index": 1},
            "sad": {"rate": 120, "voice_index": 0},
            "angry": {"rate": 200, "voice_index": 0},
            "surprise": {"rate": 190, "voice_index": 1},
            "fear": {"rate": 140, "voice_index": 0},
            "disgust": {"rate": 130, "voice_index": 0},
            "neutral": {"rate": 150, "voice_index": 0},
        }

    def speak_emotion(self, emotion_label, text="Hello, I detected a change in tone."):
        """
        Plays emotional voice cue.
        """
        profile = self.voice_profiles.get(emotion_label, self.voice_profiles["neutral"])
        try:
            self.engine.setProperty("rate", profile["rate"])
            voice = self.voices[profile["voice_index"]]
            self.engine.setProperty("voice", voice.id)
        except IndexError:
            print(f"[!] Voice index out of range for emotion: {emotion_label}")
            return

        print(f"[Clippy] ({emotion_label}) Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
