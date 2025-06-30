# User Meta-Tag Builder UI

import gradio as gr
from memory_bank_manager import add_meta_tag_to_memory, get_meta_tag_summary


def user_meta_tag_builder_ui():
    with gr.Blocks() as meta_tag_builder_ui:
        gr.Markdown("## 🏗️ User Meta-Tag Builder")

        with gr.Row():
            meta_tag_input = gr.Textbox(label="New Meta-Tag (Include brackets, e.g. [glitchy-drone])")
            sound_file_input = gr.Textbox(label="Path to Sound File (e.g. sounds/glitchy_drone.wav)")

        add_button = gr.Button("Add Meta-Tag")
        status_display = gr.Textbox(label="Status", interactive=False)

        with gr.Row():
            summary_output = gr.Textbox(label="Current Memory Bank Meta-Tags", lines=10, interactive=False)
            refresh_button = gr.Button("Refresh Meta-Tags")

        def add_meta_tag(tag, path):
            result = add_meta_tag_to_memory(tag, path)
            return result, get_meta_tag_summary()

        def refresh_summary():
            return get_meta_tag_summary()

        add_button.click(add_meta_tag, [meta_tag_input, sound_file_input], [status_display, summary_output])
        refresh_button.click(refresh_summary, None, summary_output)

    return meta_tag_builder_ui
