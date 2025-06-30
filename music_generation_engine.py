# music_generation_engine.py

from audiocraft.models import MusicGen
import os
from audio_utils import save_audio
from phoneme_and_meta_tag_utils import extract_meta_tags_from_prompt

# Set base output directory
output_directory = "generated_music"
os.makedirs(output_directory, exist_ok=True)

current_model = MusicGen.get_pretrained("facebook/musicgen-small")

def switch_music_model(model_name):
    global current_model
    print(f"[🔄] Switching to model: {model_name}")
    current_model = MusicGen.get_pretrained(model_name)
    print(f"[✔] Model switched to {model_name}")

def generate_music(prompt, duration, quality):
    print(f"[🎵] Generating music with prompt: '{prompt}' | Duration: {duration}s | Quality: {quality}")

    # Generate audio
    wav = current_model.generate([prompt], progress=True, duration=duration)

    # Extract song name
    song_name = extract_meta_tags_from_prompt(prompt).get('song_name', 'generated_song')

    # Save audio file
    audio_path = os.path.join(output_directory, f"{song_name}.wav")
    save_audio(audio_path, wav[0].cpu(), sample_rate=32000)

    print(f"[✔] Music generated and saved to {audio_path}")
    return audio_path
