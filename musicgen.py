import torch
from transformers import MusicgenForConditionalGeneration, AutoProcessor
import torchaudio
import os
from pydub import AudioSegment
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")


def convert_wav_to_format(wav_file, target_format):
    if target_format == 'wav':
        return wav_file

    target_file = wav_file.replace('.wav', f'.{target_format}')
    audio = AudioSegment.from_wav(wav_file)
    audio.export(target_file, format=target_format)
    os.remove(wav_file)
    return target_file


def adjust_generation_settings(quality_level):
    if quality_level == 'High':
        return 80
    elif quality_level == 'Medium':
        return 50
    else:
        return 30


def process_structure_tags(prompt):
    song_sections = ["[Intro]", "[Verse]", "[Chorus]", "[Bridge]", "[Hook]", "[Breakdown]", "[Outro]", "[End]", "[Big Finish]", "[Build Up]", "[Bass Drop]"]
    detected_sections = [tag for tag in song_sections if tag.lower() in prompt.lower()]
    if detected_sections:
        print(f"\n🎶 Song structure tags detected: {detected_sections}")
    return prompt


def generate_music_with_tags(prompt, duration=30, guidance_scale=3.0, filename="generated_music.wav", file_format="wav", quality="Medium", use_bark=False):
    try:
        print(f"\n🎛️ Prompt received: {prompt}")
        start_time = time.time()

        if use_bark:
            print("\n🎤 Bark Mode Enabled (To Be Implemented)")
            return None

        processed_prompt = process_structure_tags(prompt)
        inputs = processor(text=[processed_prompt], return_tensors="pt").to(device)

        token_limit = adjust_generation_settings(quality)

        print(f"\n🎹 Generating audio with quality: {quality}")
        audio_values = model.generate(
            **inputs,
            max_new_tokens=int(token_limit * duration),
            guidance_scale=guidance_scale,
        )

        elapsed_time = time.time() - start_time
        print(f"\n⏱️ Generation completed in {elapsed_time:.2f} seconds")

        audio_array = audio_values[0].cpu().numpy().squeeze()
        sampling_rate = model.config.audio_encoder.sampling_rate

        if not os.path.exists("generated_music"):
            os.makedirs("generated_music")

        wav_file = filename if filename.endswith('.wav') else filename.replace(f'.{file_format}', '.wav')
        torchaudio.save(wav_file, torch.tensor(audio_array).unsqueeze(0), sampling_rate)
        print(f"\n✅ Music saved as WAV: {wav_file}")

        final_file = convert_wav_to_format(wav_file, file_format)
        print(f"\n🎵 Final file: {final_file}")
        return final_file
    except Exception as e:
        print(f"\n🚨 Error in generate_music_with_tags: {e}")
        return None
