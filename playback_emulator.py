# playback_emulator.py

import gradio as gr
from meta_tag_soundboard import get_meta_tag_choices, play_meta_tag

def playback_emulator_interface():
    with gr.Blocks() as playback_emulator:
        gr.Markdown("## 🔉 Meta-Tag Playback Emulator")
        gr.Markdown("Preview meta-tag sounds instantly.")

        tag_selector = gr.Dropdown(choices=get_meta_tag_choices(), label="Select Meta-Tag")
        play_button = gr.Button("▶️ Play Meta-Tag Sound")
        audio_output = gr.Audio(label="Preview Audio")

        play_button.click(play_meta_tag, tag_selector, audio_output)

    return playback_emulator
