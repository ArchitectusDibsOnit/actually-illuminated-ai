# audio_event_slicer_ui.py

import gradio as gr
from audio_event_slicer import slice_audio_by_event
from system_performance import system_summary

def audio_event_slicer_interface():
    with gr.Blocks() as slicer_ui:
        gr.Markdown("## ✂️ Audio Event Slicer and Preview")

        audio_input = gr.Audio(source="upload", type="filepath", label="Upload Full Song Audio")

        target_selector = gr.Radio(choices=["song_structure", "voice_timeline"], value="song_structure", label="Select Timeline to Slice")

        slice_button = gr.Button("Slice Audio By Timeline Events")
        output_gallery = gr.Gallery(label="Audio Slices Preview", columns=2, rows=4)

        slice_button.click(slice_audio_by_event, inputs=[audio_input, target_selector], outputs=output_gallery)

        gr.Markdown(f"### 📋 System Info: {system_summary()}")

    return slicer_ui
