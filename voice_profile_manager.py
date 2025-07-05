# voice_profile_manager.py

import gradio as gr
import json
import os

VOICE_PROFILE_FILE = "voice_profiles.json"

def load_voice_profiles():
    if os.path.exists(VOICE_PROFILE_FILE):
        with open(VOICE_PROFILE_FILE, "r") as file:
            return json.load(file)
    return {}

def save_voice_profiles(profiles):
    with open(VOICE_PROFILE_FILE, "w") as file:
        json.dump(profiles, file, indent=4)

def get_available_voice_profiles():
    profiles = load_voice_profiles()
    return list(profiles.keys()) if profiles else ["No profiles — create one!"]

def voice_profile_manager_interface():
    profiles = load_voice_profiles()

    with gr.Blocks() as profile_ui:
        gr.Markdown("## 🎤 Voice Profile Manager")

        profile_selector = gr.Dropdown(choices=get_available_voice_profiles(), label="Select Voice Profile", interactive=True)
        profile_display = gr.Textbox(label="Voice Profile Details", interactive=False)

        new_profile_name = gr.Textbox(label="New Voice Profile Name")
        new_profile_data = gr.Textbox(label="Voice Profile Data (JSON)")

        save_button = gr.Button("💾 Save New Profile")
        delete_button = gr.Button("🗑️ Delete Selected Profile")

        status_output = gr.Textbox(label="Status", interactive=False)

        def save_new_profile(name, data):
            if not name.strip() or not data.strip():
                return gr.update(), "Profile name and data are required."

            try:
                parsed_data = json.loads(data)
            except json.JSONDecodeError:
                return gr.update(), "Invalid JSON format."

            profiles[name] = parsed_data
            save_voice_profiles(profiles)
            return gr.update(choices=get_available_voice_profiles()), f"Profile '{name}' saved successfully."

        def show_profile(name):
            if name == "No profiles — create one!":
                return "No profiles found. Please create one."
            return json.dumps(profiles.get(name, {}), indent=4)

        def delete_profile(name):
            if name in profiles:
                del profiles[name]
                save_voice_profiles(profiles)
                updated_profiles = get_available_voice_profiles()
                return gr.update(choices=updated_profiles), "Profile deleted."
            return gr.update(), "Profile not found."

        save_button.click(save_new_profile, [new_profile_name, new_profile_data], [profile_selector, status_output])
        profile_selector.change(show_profile, profile_selector, profile_display)
        delete_button.click(delete_profile, profile_selector, [profile_selector, status_output])

    return profile_ui
