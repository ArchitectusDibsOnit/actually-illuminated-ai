# meta_tag_soundboard.py

import gradio as gr
import os
from audio_utils import load_audio

# Define mapping of meta-tags to audio files
# You can expand this dictionary as you add sound samples
meta_tag_sounds = {
    "[guitar]": "soundboard_samples/guitar_sample.wav",
    "[drums]": "soundboard_samples/drums_sample.wav",
    "[bass]": "soundboard_samples/bass_sample.wav",
    "[explosions]": "soundboard_samples/explosion_sample.wav",
    "[vinyl crackles]": "soundboard_samples/vinyl_crackles_sample.wav",
    "[crowd noise]": "soundboard_samples/crowd_noise_sample.wav",
    "[male]": "soundboard_samples/male_voice_sample.wav",
    "[female]": "soundboard_samples/female_voice_sample.wav",
    "[robotic]": "soundboard_samples/robotic_voice_sample.wav",
    "[screaming]": "soundboard_samples/scream_sample.wav",
    # Add more as needed
}

def get_meta_tag_choices():
    return list(meta_tag_sounds.keys())

def play_meta_tag(tag):
    if tag in meta_tag_sounds and os.path.exists(meta_tag_sounds[tag]):
        return meta_tag_sounds[tag]
    else:
        return None

def meta_tag_soundboard_ui():
    with gr.Blocks() as soundboard_ui:
        gr.Markdown("## 🎛️ Meta-Tag Soundboard")

        tag_selector = gr.Dropdown(choices=get_meta_tag_choices(), label="Select Meta-Tag to Preview")
        play_button = gr.Button("▶️ Play Sound")
        audio_output = gr.Audio(label="Meta-Tag Sound Preview", interactive=False)

        play_button.click(play_meta_tag, tag_selector, audio_output)

    return soundboard_ui
