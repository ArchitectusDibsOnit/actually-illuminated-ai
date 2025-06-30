# phoneme_recorder.py

import gradio as gr
import sounddevice as sd
import soundfile as sf
import os
import time

recording_folder = "phoneme_sounds/user_recordings"

if not os.path.exists(recording_folder):
    os.makedirs(recording_folder)

def record_phoneme(phoneme_label, duration):
    if not phoneme_label:
        return "Please enter a phoneme label."

    filename = f"{recording_folder}/{phoneme_label}_{int(time.time())}.wav"

    try:
        gr.Info(f"Recording {phoneme_label} for {duration} seconds...")
        recording = sd.rec(int(duration * 44100), samplerate=44100, channels=1)
        sd.wait()
        sf.write(filename, recording, 44100)
        return f"Recording saved as {filename}"
    except Exception as e:
        return f"Recording failed: {str(e)}"

def phoneme_recorder_interface():
    with gr.Blocks() as recorder_ui:
        gr.Markdown("## 🎙️ Phoneme Recorder - Record Your Own Phoneme Sounds")

        phoneme_input = gr.Textbox(label="Phoneme Label (e.g., 'AH', 'B', 'CH')")
        duration_input = gr.Number(label="Recording Duration (seconds)", value=2.0)

        record_button = gr.Button("Start Recording")
        record_status = gr.Textbox(label="Recording Status", interactive=False)

        record_button.click(record_phoneme, [phoneme_input, duration_input], record_status)

    return recorder_ui
