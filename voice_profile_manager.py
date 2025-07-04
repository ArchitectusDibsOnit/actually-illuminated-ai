# voice_profile_manager.py

import json
import os
import gradio as gr

VOICE_PROFILE_FILE = "voice_profiles.json"

def load_voice_profiles():
    if os.path.exists(VOICE_PROFILE_FILE):
        with open(VOICE_PROFILE_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_voice_profiles(profiles):
    with open(VOICE_PROFILE_FILE, 'w') as f:
        json.dump(profiles, f, indent=4)

def get_available_voice_profiles():
    profiles = load_voice_profiles()
    return list(profiles.keys()) if profiles else ["No profiles available"]

def voice_profile_manager_interface():
    profiles = load_voice_profiles()

    profile_name = gr.Textbox(label="Voice Profile Name")
    profile_description = gr.Textbox(label="Description")
    profile_tag = gr.Textbox(label="Meta-Tag for Voice", placeholder="[male], [robotic], [alien]")

    profile_dropdown = gr.Dropdown(choices=list(profiles.keys()), label="Existing Profiles", multiselect=False)
    profile_output = gr.Textbox(label="Selected Profile Details", interactive=False)
    status = gr.Textbox(label="Status", interactive=False)

    add_button = gr.Button("➕ Add Voice Profile")
    delete_button = gr.Button("🗑️ Delete Selected Profile")

    def add_profile(name, description, tag):
        if not name.strip() or not tag.strip():
            return gr.update(choices=list(profiles.keys())), "Name and meta-tag are required."

        profiles[name] = {"description": description, "tag": tag}
        save_voice_profiles(profiles)
        return gr.update(choices=list(profiles.keys())), f"Profile '{name}' added."

    def delete_profile(name):
        if name in profiles:
            del profiles[name]
            save_voice_profiles(profiles)
            return gr.update(choices=list(profiles.keys())), f"Profile '{name}' deleted."
        return gr.update(), "Profile not found."

    def show_profile(name):
        if name in profiles:
            desc = profiles[name]["description"]
            tag = profiles[name]["tag"]
            return f"Name: {name}\nDescription: {desc}\nMeta-Tag: {tag}"
        return "Profile not found."

    add_button.click(add_profile, [profile_name, profile_description, profile_tag], [profile_dropdown, status])
    delete_button.click(delete_profile, profile_dropdown, [profile_dropdown, status])
    profile_dropdown.change(show_profile, profile_dropdown, profile_output)

    return gr.Column([
        gr.Markdown("## 🎤 Voice Profile Manager - Create, View, and Delete Profiles"),
        profile_name,
        profile_description,
        profile_tag,
        add_button,
        profile_dropdown,
        profile_output,
        delete_button,
        status
    ])
