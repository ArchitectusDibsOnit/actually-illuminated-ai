# voice_profile_manager.py

import json
import os

voice_profiles_file = "voice_profiles.json"

# Load existing profiles or create a new file
def load_voice_profiles():
    if os.path.exists(voice_profiles_file):
        with open(voice_profiles_file, "r") as file:
            return json.load(file)
    else:
        return {}

def save_voice_profiles(profiles):
    with open(voice_profiles_file, "w") as file:
        json.dump(profiles, file, indent=4)

# Gradio Interface
def voice_profile_manager_interface():
    import gradio as gr

    profiles = load_voice_profiles()

    profile_names = list(profiles.keys())

    def create_profile(name, description, voice_type, linked_phoneme_bank):
        profiles[name] = {
            "description": description,
            "voice_type": voice_type,
            "phoneme_bank": linked_phoneme_bank
        }
        save_voice_profiles(profiles)
        return gr.update(choices=list(profiles.keys())), f"Profile '{name}' created."

    def delete_profile(name):
        if name in profiles:
            del profiles[name]
            save_voice_profiles(profiles)
            return gr.update(choices=list(profiles.keys())), f"Profile '{name}' deleted."
        else:
            return gr.update(), "Profile not found."

    def view_profile(name):
        if name in profiles:
            profile = profiles[name]
            return f"Name: {name}\nDescription: {profile['description']}\nVoice Type: {profile['voice_type']}\nPhoneme Bank: {profile['phoneme_bank']}"
        else:
            return "Profile not found."

    with gr.Blocks() as voice_profile_ui:
        gr.Markdown("## 🎤 Voice Profile Manager")

        with gr.Row():
            voice_name_input = gr.Textbox(label="Voice Name")
            voice_description_input = gr.Textbox(label="Voice Description")
            voice_type_selector = gr.Dropdown(choices=["Bark", "Phoneme", "External Sample"], label="Voice Type")
            phoneme_bank_input = gr.Textbox(label="Linked Phoneme Bank")

        create_button = gr.Button("Create Voice Profile")

        profile_selector = gr.Dropdown(choices=profile_names, label="Select Voice Profile")
        delete_button = gr.Button("Delete Selected Profile")
        view_button = gr.Button("View Selected Profile")

        profile_view = gr.Textbox(label="Voice Profile Details", lines=6, interactive=False)

        create_button.click(
            create_profile,
            inputs=[voice_name_input, voice_description_input, voice_type_selector, phoneme_bank_input],
            outputs=[profile_selector, profile_view]
        )

        delete_button.click(
            delete_profile,
            inputs=[profile_selector],
            outputs=[profile_selector, profile_view]
        )

        view_button.click(
            view_profile,
            inputs=[profile_selector],
            outputs=profile_view
        )

    return voice_profile_ui

# 🔗 Utility to retrieve current voice names for timeline controller
def get_available_voice_profiles():
    return list(load_voice_profiles().keys())
