# 🎛️ voice_timeline_editor.py (Voice Timeline Editor with Sync)

import gradio as gr
import os
import time
from audio_utils import load_audio

voice_timeline = []
current_audio_file = None
audio_duration = 0


def add_voice_entry(start_time, end_time, description):
    entry = {"start": start_time, "end": end_time, "description": description}
    voice_timeline.append(entry)
    return render_timeline()


def clear_voice_timeline():
    global voice_timeline
    voice_timeline = []
    return render_timeline()


def render_timeline():
    if not voice_timeline:
        return "No voice entries defined."
    timeline_display = "\n".join([f"{entry['start']}s - {entry['end']}s: {entry['description']}" for entry in voice_timeline])
    return timeline_display


def load_audio_file(file):
    global current_audio_file, audio_duration
    if file is not None:
        audio, sr = load_audio(file.name)
        current_audio_file = file.name
        audio_duration = len(audio) / sr
        return f"Loaded: {file.name} ({audio_duration:.2f}s)"
    return "No file loaded."


def get_eta_display():
    if current_audio_file:
        return f"ETA: Estimated {audio_duration:.2f}s playback length"
    return "ETA: No audio loaded."


def voice_timeline_editor_interface():
    with gr.Blocks() as timeline_ui:
        gr.Markdown("## 🎼 Voice Timeline Editor with Synchronization")

        audio_input = gr.Audio(label="Upload Generated Song", type="filepath")
        load_status = gr.Textbox(label="Audio Load Status", interactive=False)

        load_button = gr.Button("Load Audio File")
        eta_display = gr.Textbox(label="Estimated Duration", interactive=False)

        with gr.Row():
            start_input = gr.Number(label="Start Time (seconds)")
            end_input = gr.Number(label="End Time (seconds)")
            description_input = gr.Textbox(label="Voice Description")

        add_button = gr.Button("Add Voice Segment")
        clear_button = gr.Button("Clear Timeline")

        timeline_output = gr.Textbox(label="Voice Timeline", lines=10, interactive=False)

        load_button.click(load_audio_file, audio_input, load_status)
        load_button.click(lambda: get_eta_display(), None, eta_display)

        add_button.click(add_voice_entry, [start_input, end_input, description_input], timeline_output)
        clear_button.click(clear_voice_timeline, None, timeline_output)

    return timeline_ui
