# 🔉 Real-Time Meta-Tag Playback Emulator - Backend Integration

import gradio as gr
import os
import random
import torchaudio
from audio_utils import load_audio
from phoneme_and_meta_tag_utils import meta_tags

# Directory where phoneme and meta-tag sounds are stored
SOUNDS_DIRECTORY = "phoneme_sounds"

def list_available_sounds():
    if not os.path.exists(SOUNDS_DIRECTORY):
        return []
    return [f for f in os.listdir(SOUNDS_DIRECTORY) if f.endswith('.wav')]

def get_sound_path(sound_name):
    return os.path.join(SOUNDS_DIRECTORY, sound_name)

def preview_sound(sound_name):
    sound_path = get_sound_path(sound_name)
    if os.path.exists(sound_path):
        return sound_path
    return None

def playback_emulator_interface():
    with gr.Blocks() as playback_emulator:
        gr.Markdown("## 🔉 Meta-Tag Playback Emulator")
        gr.Markdown("Test and preview available meta-tag sounds in real-time.")

        sound_choices = list_available_sounds()
        if not sound_choices:
            sound_choices = ["No sounds found. Please add .wav files to the phoneme_sounds folder."]

        sound_selector = gr.Dropdown(choices=sound_choices, label="Select Meta-Tag Sound")
        preview_button = gr.Button("▶️ Play Sound")
        audio_output = gr.Audio(label="Sound Preview", interactive=False)

        preview_button.click(preview_sound, sound_selector, audio_output)

    return playback_emulator
