# phoneme_editor.py

import gradio as gr
from phoneme_and_meta_tag_utils import load_phoneme_profiles, save_meta_tags

phoneme_profiles = {}

def add_phoneme_profile(name, phoneme_style, pitch, meta_tags):
    phoneme_profiles[name] = {
        "phoneme_style": phoneme_style,
        "pitch": pitch,
        "meta_tags": meta_tags
    }
    return f"Profile '{name}' added successfully."

def delete_phoneme_profile(name):
    if name in phoneme_profiles:
        del phoneme_profiles[name]
        return f"Profile '{name}' deleted."
    return f"Profile '{name}' not found."

def phoneme_editor_interface():
    with gr.Blocks() as editor_ui:
        gr.Markdown("## 🎤 Phoneme Editor")

        with gr.Row():
            profile_name = gr.Textbox(label="Profile Name")
            phoneme_style = gr.Textbox(label="Phoneme Style (e.g., sharp, soft)")
            pitch = gr.Slider(label="Pitch", minimum=-12, maximum=12, value=0)
            meta_tags = gr.Textbox(label="Meta-Tags (space-separated)")

        add_button = gr.Button("Add Profile")
        delete_button = gr.Button("Delete Profile")

        status_display = gr.Textbox(label="Status", interactive=False)

        add_button.click(add_phoneme_profile, [profile_name, phoneme_style, pitch, meta_tags], status_display)
        delete_button.click(delete_phoneme_profile, profile_name, status_display)

    return editor_ui
