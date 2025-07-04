# frame_slicer.py (Real-Time Progress & ETA Integrated)

import time
from audiocraft.models import MusicGen
import os
from audio_utils import save_audio
from phoneme_and_meta_tag_utils import extract_meta_tags_from_prompt
import numpy as np
from scipy.io.wavfile import write as write_wav

output_directory = "generated_music"
os.makedirs(output_directory, exist_ok=True)

current_model = MusicGen.get_pretrained("facebook/musicgen-small")


def frame_sliced_generate(prompt, total_duration, quality, progress=None, eta_display=None, progress_bar=None):
    print(f"[⚙️] Starting frame-sliced generation. Total Duration: {total_duration}s")

    slice_size = 6  # Fixed slice size for now
    slices = total_duration // slice_size + (1 if total_duration % slice_size else 0)
    remaining = total_duration % slice_size
    generated_slices = []
    estimated_time_per_slice = 20  # Adjust based on your system

    start_time = time.time()

    for i in range(int(slices)):
        print(f"[⏳] Generating slice {i + 1}/{int(slices)}")

        current_slice = slice_size if (i < slices - 1 or remaining == 0) else remaining
        generated = current_model.generate([prompt], progress=True)

        generated_slices.append(generated[0].cpu().numpy())

        if progress_bar:
            progress_bar.value = int(((i + 1) / slices) * 100)
        if eta_display:
            elapsed = time.time() - start_time
            eta_remaining = max(int((slices - (i + 1)) * estimated_time_per_slice - elapsed), 0)
            eta_display.value = f"{eta_remaining} seconds remaining."

    final_audio = np.concatenate(generated_slices)
    final_audio = final_audio / np.max(np.abs(final_audio))  # Normalize to prevent clipping

    song_name = extract_meta_tags_from_prompt(prompt)
    if isinstance(song_name, dict):
        song_name = song_name.get('song_name', 'generated_song')
    else:
        song_name = 'generated_song'

    audio_path = os.path.join(output_directory, f"{song_name}_sliced.wav")
    write_wav(audio_path, 32000, final_audio)

    print(f"[✔] Frame-sliced generation complete. File saved at {audio_path}")
    return audio_path
