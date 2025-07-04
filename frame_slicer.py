# frame_slicer.py

import os
import numpy as np
from audio_utils import save_audio
from music_generation_engine import generate_music
from uuid import uuid4
import time

# Output directory for frame-sliced files
output_directory = "frame_sliced_output"
os.makedirs(output_directory, exist_ok=True)

def frame_sliced_generate(prompt, total_duration, quality, slice_duration=6, progress_callback=None):
    """
    Generates music in frame slices and stitches them into a single audio file.
    """
    slices = []
    num_slices = total_duration // slice_duration
    remainder = total_duration % slice_duration
    song_id = str(uuid4())
    final_audio_path = os.path.join(output_directory, f"{song_id}_stitched.wav")

    total_steps = num_slices + (1 if remainder else 0)
    step_counter = 1

    for i in range(num_slices):
        if progress_callback:
            progress_callback(f"Generating slice {step_counter}/{total_steps}...")
        slice_audio_path = generate_music(prompt, slice_duration, quality)
        audio_slice, sr = load_audio(slice_audio_path)
        slices.append(audio_slice)
        step_counter += 1

    if remainder > 0:
        if progress_callback:
            progress_callback(f"Generating final slice {step_counter}/{total_steps}...")
        slice_audio_path = generate_music(prompt, remainder, quality)
        audio_slice, sr = load_audio(slice_audio_path)
        slices.append(audio_slice)

    if slices:
        combined_audio = np.concatenate(slices)
        save_audio(final_audio_path, combined_audio, sr)
        if progress_callback:
            progress_callback(f"[✔] Frame-sliced generation complete!")
        return final_audio_path
    else:
        if progress_callback:
            progress_callback(f"[❌] No audio generated.")
        return None
