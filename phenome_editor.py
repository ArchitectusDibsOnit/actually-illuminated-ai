 # phoneme_editor.py

import gradio as gr
from phoneme_and_meta_tag_utils import (
    load_phoneme_profiles, save_phoneme_profile, delete_phoneme_profile
)

def phoneme_editor_interface():
    profiles = load_phoneme_profiles()

    name_input = gr.Textbox(label="Profile Name")
    phoneme_input = gr.Textbox(label="Phoneme Sequence (space-separated)")
    save_btn = gr.Button("💾 Save Profile")
    profile_dropdown = gr.Dropdown(choices=list(profiles.keys()), label="Saved Profiles")
    output = gr.Textbox(label="Status / Profile Data", interactive=False)
    delete_btn = gr.Button("🗑️ Delete Profile")

    def save_profile(name, seq):
        if not name or not seq:
            return "Name and sequence are required."
        save_phoneme_profile(name, seq)
        return f"Saved '{name}': {seq}"

    def load_profile(name):
        profiles = load_phoneme_profiles()
        if name in profiles:
            return profiles[name]
        return "Profile not found."

    def delete_profile(name):
        success = delete_phoneme_profile(name)
        return "Deleted." if success else "Not found."

    save_btn.click(save_profile, [name_input, phoneme_input], output)
    profile_dropdown.change(load_profile, profile_dropdown, phoneme_input)
    profile_dropdown.change(load_profile, profile_dropdown, output)
    delete_btn.click(delete_profile, profile_dropdown, output)

    return gr.Column([
        gr.Markdown("## 🔊 Phoneme Editor"),
        name_input, phoneme_input, save_btn,
        profile_dropdown, output, delete_btn
    ])
