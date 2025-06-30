# multi_voice_audio_splitter.py

import torchaudio
import os

def split_multivoice_audio(input_audio_path, timeline_log):
    waveform, sample_rate = torchaudio.load(input_audio_path)
    output_dir = "voice_splits"
    os.makedirs(output_dir, exist_ok=True)

    split_paths = []

    for idx, entry in enumerate(timeline_log):
        start_sample = int(entry["start_time"] * sample_rate)
        end_sample = int(entry["end_time"] * sample_rate)
        voice_waveform = waveform[:, start_sample:end_sample]

        split_path = os.path.join(output_dir, f"{entry['voice'].replace(' ', '_')}_part{idx+1}.wav")
        torchaudio.save(split_path, voice_waveform, sample_rate)
        split_paths.append(split_path)

    print(f"[✔] Voice segments exported: {split_paths}")
    return split_paths
