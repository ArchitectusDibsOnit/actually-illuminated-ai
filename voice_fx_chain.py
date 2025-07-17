# voice_fx_chain.py
# Modular voice FX chain (pitch shift, robotize, reverb, etc)

import os
from pydub import AudioSegment
import librosa
import soundfile as sf


def apply_fx_chain(audio_path, fx_config):
    """
    Applies a configurable set of audio effects.
    fx_config = {
        "pitch_shift": -3,
        "reverb": True,
        "robotize": True
    }
    """
    # Load audio
    audio = AudioSegment.from_file(audio_path)
    tmp_wav = "tmp_fx.wav"
    audio.export(tmp_wav, format="wav")

    # Convert to numpy array
    y, sr = librosa.load(tmp_wav, sr=None)

    # Pitch Shift
    if fx_config.get("pitch_shift"):
        y = librosa.effects.pitch_shift(y, sr, n_steps=fx_config["pitch_shift"])

    # Robotize (via ring modulation)
    if fx_config.get("robotize"):
        import numpy as np
        t = np.linspace(0, len(y) / sr, len(y))
        y = y * np.sign(np.sin(2 * np.pi * 30 * t))

    # Save processed output
    processed_path = audio_path.replace(".wav", "_fx.wav")
    sf.write(processed_path, y, sr)

    return processed_path
