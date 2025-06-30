# chadgpetey_voice_generator.py

import os
import soundfile as sf
import sounddevice as sd
from bark import SAMPLE_RATE, generate_audio

output_folder = "phoneme_sounds/chadgpetey"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

starter_phonemes = ['AH', 'B', 'CH', 'D', 'EH', 'F', 'G', 'HH', 'IH', 'JH', 'K', 'L', 'M', 'N', 'OW', 'P', 'R', 'S', 'T', 'UH', 'V', 'W', 'Y', 'Z']

def generate_phoneme_with_bark(phoneme):
    print(f"Generating {phoneme}...")
    audio_array = generate_audio(f"{phoneme} sound.")
    file_path = f"{output_folder}/{phoneme}.wav"
    sf.write(file_path, audio_array, SAMPLE_RATE)
    return f"Generated: {file_path}"

def generate_chadgpetey_phoneme_set():
    for phoneme in starter_phonemes:
        generate_phoneme_with_bark(phoneme)
    return "✅ Chad G. Petey Starter Phoneme Set Generated Successfully."
