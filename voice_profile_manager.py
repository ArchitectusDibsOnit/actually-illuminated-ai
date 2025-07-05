# voice_profile_manager.py

import gradio as gr
import json
import os

VOICE_PROFILE_FILE = "voice_profiles.json"

def load_voice_profiles():
    if os.path.exists(VOICE_PROFILE_FILE):
        with open(VOICE_PROFILE_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_voice_profiles(profiles):
    with open(VOICE_PROFILE_FILE, 'w') as file:
        json.dump(profiles, file, indent=4)

def get_available_voice_profiles():
    profiles = load_voice_profiles()
    return list(profiles.keys())

def voice_profile_manager_interface():
    with gr.Blocks() as voice_ui:
        gr.Markdown("## 🎙️ Voice Profile Manager")

        profiles = load_voice_profiles()

        profile_selector = gr.Dropdown(choices=get_available_voice_profiles(), label="Select Existing Voice Profile", interactive=True)
        profile_output = gr.Textbox(label="Voice Profile Details", lines=10, interactive=False)

        with gr.Row():
            new_profile_name = gr.Textbox(label="New Profile Name")
            phoneme_style = gr.Textbox(label="Phoneme Style")
            pitch_setting = gr.Number(label="Pitch Setting", value=1.0)
            meta_tags = gr.Textbox(label="Associated Meta-Tags (space-separated)")

        save_button = gr.Button("💾 Save Profile")
        delete_button = gr.Button("🗑️ Delete Selected Profile")

        def save_profile(name, phonemes, pitch, tags):
            if not name:
                return gr.update(), "Profile name is required."

            profiles[name] = {
                "phoneme_style": phonemes,
                "pitch": pitch,
                "meta_tags": tags.strip()
            }
            save_voice_profiles(profiles)
            return gr.update(choices=get_available_voice_profiles(), value=name), f"Profile '{name}' saved."

        def load_profile(name):
            profile = profiles.get(name)
            if profile:
                return f"Phoneme Style: {profile['phoneme_style']}\nPitch: {profile['pitch']}\nMeta-Tags: {profile['meta_tags']}"
            return "Profile not found."

        def delete_profile(name):
            if name in profiles:
                del profiles[name]
                save_voice_profiles(profiles)
                return gr.update(choices=get_available_voice_profiles(), value=None), "Profile deleted."
            return gr.update(), "Profile not found."

        save_button.click(save_profile, [new_profile_name, phoneme_style, pitch_setting, meta_tags], [profile_selector, profile_output])
        delete_button.click(delete_profile, profile_selector, [profile_selector, profile_output])
        profile_selector.change(load_profile, profile_selector, profile_output)

    return voice_ui
