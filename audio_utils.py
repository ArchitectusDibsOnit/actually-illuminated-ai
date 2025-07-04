# audio_utils.py

import numpy as np
import soundfile as sf
import librosa
import torchaudio
import torch
import os

def save_audio(filename, audio_array, sampling_rate):
    sf.write(filename, audio_array, sampling_rate)

def load_audio(filename, target_sr=16000):
    if filename.endswith('.wav'):
        audio, sr = librosa.load(filename, sr=target_sr)
        return audio, sr
    else:
        waveform, sample_rate = torchaudio.load(filename)
        return waveform, sample_rate

def normalize_audio(audio_array):
    return audio_array / np.max(np.abs(audio_array))

def pitch_shift(audio_array, sr, n_steps):
    return librosa.effects.pitch_shift(audio_array, sr, n_steps)

def time_stretch(audio_array, rate):
    return librosa.effects.time_stretch(audio_array, rate)

def apply_reverb(audio_array, sr, reverberance=50):
    impulse_response = np.zeros(int(sr * 0.1))
    impulse_response[0] = 1.0
    impulse_response[int(sr * 0.05)] = reverberance / 100.0
    reverbed = np.convolve(audio_array, impulse_response, mode='full')
    return reverbed[:len(audio_array)]

def convert_to_wav(input_path, output_path):
    waveform, sample_rate = load_audio(input_path)
    save_audio(output_path, waveform.numpy().squeeze(), sample_rate)
