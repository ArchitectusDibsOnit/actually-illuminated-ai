# phoneme_playback_engine.py

import gradio as gr
import numpy as np
import soundfile as sf
import librosa
import random
import os

from phoneme_and_meta_tag_utils import load_phoneme_profiles, apply_voice_morphing

# 🔊 Phoneme-to-Sound Mapping
PHONEME_SOUNDS = {
    'æ': 'assets/phoneme_sounds/ae.wav',
    'b': 'assets/phoneme_sounds/b.wav',
    'k': 'assets/phoneme_sounds/k.wav',
    'd': 'assets/phoneme_sounds/d.wav',
    'ɛ': 'assets/phoneme_sounds/eh.wav',
    'f': 'assets/phoneme_sounds/f.wav',
    'ɡ': 'assets/phoneme_sounds/g.wav',
    'h': 'assets/phoneme_sounds/h.wav',
    'ɪ': 'assets/phoneme_sounds/ih.wav',
    'dʒ': 'assets/phoneme_sounds/j.wav',
    'l': 'assets/phoneme_sounds/l.wav',
    'm': 'assets/phoneme_sounds/m.wav',
    'n': 'assets/phoneme_sounds/n.wav',
    'ɔ': 'assets/phoneme_sounds/aw.wav',
    'p': 'assets/phoneme_sounds/p.wav',
    'kw': 'assets/phoneme_sounds/kw.wav',
    'ɹ': 'assets/phoneme_sounds/r.wav',
    's': 'assets/phoneme_sounds/s.wav',
    't': 'assets/phoneme_sounds/t.wav',
    'ʊ': 'assets/phoneme_sounds/uh.wav',
    'v': 'assets/phoneme_sounds/v.wav',
    'w': 'assets/phoneme_sounds/w.wav',
    'ks': 'assets/phoneme_sounds/ks.wav',
    'j': 'assets/phoneme_sounds/y.wav',
    'z': 'assets/phoneme_sounds/z.wav'
}

def concatenate_audio(audio_paths):
    combined_audio = np.array([], dtype=np.float32)
    for path in audio_paths:
        if os.path.exists(path):
            audio, sr = librosa.load(path, sr=None)
            combined_audio = np.concatenate((combined_audio, audio))
    return combined_audio, sr

def generate_phoneme_audio_sequence(phoneme_sequence):
    phonemes = phoneme_sequence.split()
    audio_paths = []

    for phoneme in phonemes:
        if phoneme in PHONEME_SOUNDS:
            audio_paths.append(PHONEME_SOUNDS[phoneme])

    if not audio_paths:
        return None

    combined_audio, sr = concatenate_audio(audio_paths)

    output_path = "generated_music/phoneme_preview.wav"
    sf.write(output_path, combined_audio, sr)
    return output_path

def phoneme_playback_interface():
    phoneme_profiles = load_phoneme_profiles()

    with gr.Blocks() as phoneme_playback_ui:
        gr.Markdown("## 🎙️ Phoneme Voice Playback System")

        profile_selector = gr.Dropdown(choices=list(phoneme_profiles.keys()), label="Select Phoneme Profile")
        morph_strength_slider = gr.Slider(0.0, 1.0, value=0.0, step=0.01, label="Morphing Strength")

        with gr.Row():
            phoneme_display = gr.Textbox(label="Phoneme Sequence", interactive=False)
            play_button = gr.Button("▶️ Play Phoneme Sequence")

        audio_output = gr.Audio(label="Phoneme Playback Preview")

        def play_profile(profile_name, morph_strength):
            phoneme_sequence = phoneme_profiles.get(profile_name)
            if morph_strength > 0:
                phoneme_sequence = apply_voice_morphing(phoneme_sequence, morph_strength)
            phoneme_display_value = phoneme_sequence
            audio_path = generate_phoneme_audio_sequence(phoneme_sequence)
            return phoneme_display_value, audio_path

        play_button.click(
            play_profile,
            inputs=[profile_selector, morph_strength_slider],
            outputs=[phoneme_display, audio_output]
        )

    return phoneme_playback_ui
