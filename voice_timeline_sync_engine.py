# voice_timeline_sync_engine.py

from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import os

current_model = None

def load_timeline_music_model():
    global current_model
    current_model = MusicGen.get_pretrained('facebook/musicgen-large')
    return current_model

def synchronize_voice_timeline(prompt, duration, quality, timeline_log):
    if current_model is None:
        load_timeline_music_model()

    print(f"[🎛️ Syncing Voice Timeline]")
    print(f"Voice Timeline Entries: {timeline_log}")

    print(f"[🎵] Generating music with prompt: '{prompt}' | Duration: {duration}s | Quality: {quality}")
    wav_output = current_model.generate([prompt], progress=True, duration=duration)

    output_dir = "generated_music"
    os.makedirs(output_dir, exist_ok=True)

    sanitized_filename = prompt.strip().split('\n')[0].replace(' ', '_').replace('/', '_')[:50]
    output_path = os.path.join(output_dir, f"{sanitized_filename}_synced.wav")

    audio_write(output_path, wav_output[0].cpu(), current_model.sample_rate, strategy="loudness", loudness_compressor=True)
    print(f"[✔] Synced music saved to: {output_path}")

    return output_path
