# export_manager.py

import os
import shutil

EXPORT_FOLDER = "exports"

def export_generated_song(song_file_path, export_format="wav"):
    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)

    song_name = os.path.basename(song_file_path)
    base_name, _ = os.path.splitext(song_name)
    export_path = os.path.join(EXPORT_FOLDER, f"{base_name}.{export_format}")

    # For now, we simply copy the file as a demonstration (format conversion can be added later)
    shutil.copy(song_file_path, export_path)

    return export_path

def export_manager_interface():
    import gradio as gr

    with gr.Row():
        song_file_input = gr.Textbox(label="Enter Path of Generated Song")
        export_format = gr.Dropdown(choices=["wav", "mp3", "ogg", "flac"], label="Export Format", value="wav")

    export_button = gr.Button("Export Song")
    export_status = gr.Textbox(label="Export Status", interactive=False)

    def export_song(song_path, format_choice):
        try:
            export_path = export_generated_song(song_path, export_format=format_choice)
            return f"Song successfully exported to: {export_path}"
        except Exception as e:
            return f"Export failed: {str(e)}"

    export_button.click(
        fn=export_song,
        inputs=[song_file_input, export_format],
        outputs=export_status
    )

    return gr.Column([
        gr.Markdown("## 📤 Export Manager"),
        song_file_input,
        export_format,
        export_button,
        export_status
    ])
