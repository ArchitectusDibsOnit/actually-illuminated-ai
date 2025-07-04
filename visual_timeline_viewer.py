# visual_timeline_viewer.py

import gradio as gr
from song_structure_manager import display_timeline
from voice_timeline_sync_engine import render_voice_timeline
from timeline_file_manager import save_timelines, load_timelines, list_saved_timelines

def visual_timeline_viewer_interface():
    with gr.Blocks() as visual_ui:
        gr.Markdown("## 🎛️ Visual Timeline Viewer")

        with gr.Tabs():
            with gr.TabItem("Song Structure Timeline"):
                song_structure_output = gr.Textbox(label="Song Structure Timeline", lines=12, interactive=False)
                song_structure_output.value = display_timeline()

            with gr.TabItem("Voice Timeline"):
                voice_timeline_output = gr.Textbox(label="Voice Timeline", lines=12, interactive=False)
                voice_timeline_output.value = render_voice_timeline()

        with gr.Row():
            save_filename_input = gr.Textbox(label="Save As (Filename)", value="timeline_save")
            save_button = gr.Button("💾 Save Timelines")

            file_selector = gr.Dropdown(choices=list_saved_timelines(), label="Select Save File", interactive=True)
            refresh_button = gr.Button("🔄 Refresh List")
            load_button = gr.Button("📂 Load Selected File")

            status_output = gr.Textbox(label="Status", interactive=False)

        save_button.click(fn=save_timelines, inputs=save_filename_input, outputs=status_output)
        refresh_button.click(fn=lambda: gr.update(choices=list_saved_timelines()), inputs=None, outputs=file_selector)
        load_button.click(fn=load_timelines, inputs=file_selector, outputs=status_output)

    return visual_ui
