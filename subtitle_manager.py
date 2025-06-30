# subtitle_manager.py

import gradio as gr
import whisper
import os
from audio_utils import load_audio

transcribed_text = ""
current_subtitles = []


def transcribe_audio(file):
    global transcribed_text, current_subtitles
    if file is not None:
        model = whisper.load_model("base")
        result = model.transcribe(file.name)
        transcribed_text = result['text']
        current_subtitles = generate_subtitles(result['segments'])
        return transcribed_text
    return "No file loaded."


def generate_subtitles(segments):
    subtitles = []
    for segment in segments:
        start = format_time(segment['start'])
        end = format_time(segment['end'])
        text = segment['text']
        subtitles.append(f"{start} --> {end}\n{text}")
    return subtitles


def format_time(seconds):
    millis = int((seconds - int(seconds)) * 1000)
    secs = int(seconds % 60)
    mins = int((seconds // 60) % 60)
    hours = int((seconds // 3600))
    return f"{hours:02}:{mins:02}:{secs:02},{millis:03}"


def export_subtitles():
    if not current_subtitles:
        return "No subtitles to export."
    if not os.path.exists("generated_subtitles"):
        os.makedirs("generated_subtitles")
    filename = f"generated_subtitles/subtitles_{len(os.listdir('generated_subtitles')) + 1}.srt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(current_subtitles))
    return f"Subtitles exported to: {filename}"


def clear_subtitles():
    global transcribed_text, current_subtitles
    transcribed_text = ""
    current_subtitles = []
    return "", "Subtitles cleared."


def subtitle_manager_interface():
    with gr.Blocks() as subtitle_ui:
        gr.Markdown("## 🎬 Subtitle Manager - Transcribe and Manage Subtitles")

        audio_input = gr.Audio(label="Upload Audio for Transcription", type="filepath")
        transcribe_button = gr.Button("Transcribe Audio")
        export_button = gr.Button("Export Subtitles")
        clear_button = gr.Button("Clear Subtitles")

        transcribed_output = gr.Textbox(label="Transcribed Text", lines=10, interactive=False)
        export_status = gr.Textbox(label="Export Status", interactive=False)

        transcribe_button.click(transcribe_audio, audio_input, transcribed_output)
        export_button.click(lambda: export_subtitles(), None, export_status)
        clear_button.click(clear_subtitles, None, [transcribed_output, export_status])

    return subtitle_ui
