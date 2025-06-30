# phoneme_sound_manager.py (Add/Update)

import gradio as gr
import os
import sounddevice as sd
import soundfile as sf

phoneme_folder = "phoneme_sounds/chadgpetey"

def list_phoneme_files():
    if not os.path.exists(phoneme_folder):
        return []
    return [f for f in os.listdir(phoneme_folder) if f.endswith(".wav")]

def play_phoneme(phoneme_file):
    if phoneme_file:
        file_path = os.path.join(phoneme_folder, phoneme_file)
        audio, sr = sf.read(file_path)
        sd.play(audio, sr)
        sd.wait()
        return f"Playing: {phoneme_file}"
    return "No file selected."

def phoneme_sound_manager_interface():
    phoneme_files = list_phoneme_files()

    with gr.Blocks() as phoneme_manager_ui:
        gr.Markdown("## 🎧 Phoneme Sound Manager - Playback Tester")

        phoneme_dropdown = gr.Dropdown(choices=phoneme_files, label="Select Phoneme Sound")
        play_button = gr.Button("Play Phoneme")

        playback_status = gr.Textbox(label="Playback Status", interactive=False)

        play_button.click(play_phoneme, phoneme_dropdown, playback_status)

    return phoneme_manager_ui
