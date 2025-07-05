# music_generation_engine.py (Optimized with Caching and Multiprocessing)

from audiocraft.models import MusicGen
import os
from audio_utils import save_audio
from phoneme_and_meta_tag_utils import extract_meta_tags_from_prompt
from multiprocessing import Pool, cpu_count

# Set base output directory
output_directory = "generated_music"
os.makedirs(output_directory, exist_ok=True)

current_model = None
current_model_name = None

def load_music_model(model_name):
    global current_model, current_model_name
    if current_model_name != model_name:
        print(f"[🔄] Loading model: {model_name}")
        current_model = MusicGen.get_pretrained(model_name)
        current_model_name = model_name
        print(f"[✔] Model {model_name} loaded successfully.")

def switch_music_model(model_name):
    load_music_model(model_name)

def generate_music(prompt, duration, quality):
    print(f"[🎵] Generating music with prompt: '{prompt}' | Quality: {quality}")
    if current_model is None:
        load_music_model("facebook/musicgen-small")  # Load default if not already loaded

    try:
        wav = current_model.generate([prompt], progress=True)

        song_name = extract_meta_tags_from_prompt(prompt)
        if isinstance(song_name, dict):
            song_name = song_name.get('song_name', 'generated_song')
        else:
            song_name = 'generated_song'

        audio_path = os.path.join(output_directory, f"{song_name}.wav")
        save_audio(audio_path, wav[0].cpu(), sample_rate=32000)

        print(f"[✔] Music generated and saved to {audio_path}")
        return audio_path

    except Exception as e:
        print(f"[❌] Generation failed: {e}")
        return None

# Multiprocessing frame-sliced generator
def generate_slice(args):
    prompt, quality = args
    try:
        wav = current_model.generate([prompt], progress=True)
        return wav[0].cpu()
    except Exception as e:
        print(f"[❌] Slice generation failed: {e}")
        return None

def frame_sliced_generate(prompt, duration, quality, slice_size=6):
    print(f"[⚙️] Frame slicing active: {duration}s split into {slice_size}s segments.")
    slices = []
    num_slices = duration // slice_size + (1 if duration % slice_size else 0)

    slice_prompts = [prompt for _ in range(num_slices)]

    with Pool(processes=min(cpu_count(), num_slices)) as pool:
        results = pool.map(generate_slice, [(sp, quality) for sp in slice_prompts])

    for audio in results:
        if audio is not None:
            slices.append(audio)

    if not slices:
        print("[❌] No slices generated successfully.")
        return None

    final_audio = sum(slices)
    song_name = extract_meta_tags_from_prompt(prompt)
    if isinstance(song_name, dict):
        song_name = song_name.get('song_name', 'generated_song')
    else:
        song_name = 'generated_song'

    audio_path = os.path.join(output_directory, f"{song_name}_sliced.wav")
    save_audio(audio_path, final_audio, sample_rate=32000)

    print(f"[✔] Frame-sliced audio saved to {audio_path}")
    return audio_path
