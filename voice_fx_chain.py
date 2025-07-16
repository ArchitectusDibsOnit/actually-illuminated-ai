# voice_fx_chain.py (Voice FX Processor for GlyphClippy)

import os
import tempfile
from pydub import AudioSegment
import librosa
import soundfile as sf

# -- Helper: Apply pitch shift with librosa --
def apply_pitch_shift(input_path, n_steps):
    y, sr = librosa.load(input_path, sr=None)
    y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=n_steps)
    output_path = tempfile.mktemp(suffix="_pitch.wav")
    sf.write(output_path, y_shifted, sr)
    return output_path

# -- Helper: Apply robotize FX using pydub --
def apply_robot_fx(input_path):
    sound = AudioSegment.from_file(input_path)
    robotized = sound.low_pass_filter(300).high_pass_filter(300).overlay(sound.reverse())
    output_path = tempfile.mktemp(suffix="_robot.wav")
    robotized.export(output_path, format="wav")
    return output_path

# -- Main: Apply FX chain --
def apply_voice_fx(input_wav, pitch=0, robotize=False):
    current_path = input_wav

    if pitch != 0:
        current_path = apply_pitch_shift(current_path, pitch)

    if robotize:
        current_path = apply_robot_fx(current_path)

    return current_path

# Example usage:
# fx_applied = apply_voice_fx("input.wav", pitch=2, robotize=True)
