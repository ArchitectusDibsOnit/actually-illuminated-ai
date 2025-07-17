# tts_pipeline.py (TTS + Emotion + Voice FX)

import os
import random
from pathlib import Path
import pyttsx3  # fallback only
import soundfile as sf
import librosa

from voice_fx_chain import apply_voice_effects
from emotion_detector import detect_emotion

try:
    import openvoice
    openvoice_available = True
except ImportError:
    openvoice_available = False

TTS_OUTPUT_DIR = "tts_output"
os.makedirs(TTS_OUTPUT_DIR, exist_ok=True)

def speak_text(text, emotion_hint="Neutral", voice_profile=None, effects_chain=None):
    """
    Generate TTS audio with optional emotional hint and FX processing.
    Returns path to final WAV.
    """
    base_filename = f"clippy_speak_{random.randint(1000,9999)}.wav"
    output_path = os.path.join(TTS_OUTPUT_DIR, base_filename)

    if openvoice_available and voice_profile:
        try:
            # Use OpenVoice TTS
            tts_wav = openvoice.speak(text, speaker=voice_profile, emotion=emotion_hint)
            sf.write(output_path, tts_wav, samplerate=44100)
        except Exception as e:
            print(f"[OpenVoice] Error: {e}. Falling back to pyttsx3.")
            _speak_fallback(text, output_path)
    else:
        _speak_fallback(text, output_path)

    # Apply FX chain if any
    if effects_chain:
        y, sr = librosa.load(output_path, sr=44100)
        y_fx = apply_voice_effects(y, sr, effects_chain)
        sf.write(output_path, y_fx, sr)

    return output_path

def _speak_fallback(text, output_path):
    engine = pyttsx3.init()
    engine.setProperty('rate', 185)
    engine.save_to_file(text, output_path)
    engine.runAndWait()

# Example callable
if __name__ == "__main__":
    test_text = "The glyph reactor is nearly online."
    emotion = detect_emotion(test_text)
    print(f"Detected: {emotion}")
    final_wav = speak_text(test_text, emotion_hint=emotion, effects_chain=["robotize", "pitch-3"])
    print(f"Saved to: {final_wav}")
