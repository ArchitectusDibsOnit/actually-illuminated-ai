# audio_event_slicer.py

import os
import librosa
import soundfile as sf

from song_structure_manager import timeline as song_timeline
from voice_timeline_sync_engine import voice_timeline

SLICES_FOLDER = "audio_slices"
os.makedirs(SLICES_FOLDER, exist_ok=True)

def slice_audio_by_event(audio_path, target="song_structure"):
    if not os.path.exists(audio_path):
        return "❌ Audio file not found."

    y, sr = librosa.load(audio_path, sr=None)
    slices = []

    if target == "song_structure":
        target_timeline = song_timeline
    elif target == "voice_timeline":
        target_timeline = voice_timeline
    else:
        return "❌ Invalid timeline target."

    for idx, event in enumerate(target_timeline):
        start_sample = int(event["start"] * sr)
        end_sample = int(event["end"] * sr)
        audio_slice = y[start_sample:end_sample]

        slice_filename = os.path.join(SLICES_FOLDER, f"{target}_slice_{idx+1}.wav")
        sf.write(slice_filename, audio_slice, sr)
        slices.append(slice_filename)

    return slices
