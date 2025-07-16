# subtitle_ui.py (with Emotion Glyph Display)

import os
import gradio as gr
from subtitle_manager import transcribe_audio, save_subtitles, get_subtitles, auto_generate_phonemes
from phoneme_and_meta_tag_utils import text_to_phonemes

emotion_glyphs = {
    "Happy": "😊",
    "Sad": "😢",
    "Angry": "😠",
    "Surprise": "😲",
    "Fear": "😨",
    "Disgust": "🤢",
    "Neutral": "😐"
}

def subtitle_interface():
    with gr.Blocks() as subtitle_ui:
        gr.Markdown("## 📝 Subtitle Manager + Phoneme Generator + Emotion Tags")

        with gr.Row():
            audio_input = gr.Audio(type="filepath", label="Upload Audio File")

        transcribed_output = gr.Textbox(label="Transcribed Subtitles", lines=6)
        emotion_output = gr.Textbox(label="Detected Emotion", lines=1, interactive=False)
        phoneme_output = gr.Textbox(label="Auto-Generated Phonemes", lines=6, interactive=False)

        with gr.Row():
            transcribe_button = gr.Button("Transcribe Audio")
            clear_button = gr.Button("Clear")

        with gr.Row():
            save_button = gr.Button("Save Subtitles and Phonemes")

        def handle_transcription(audio_path):
            text, segments = transcribe_audio(audio_path)
            all_emotions = [seg.get("emotion", "Neutral") for seg in segments]
            most_common = max(set(all_emotions), key=all_emotions.count)
            glyph = emotion_glyphs.get(most_common, "😐")
            return text, f"{glyph} {most_common}"

        def handle_clear():
            return "", "", ""

        def handle_save(audio_path, text):
            audio_name = os.path.basename(audio_path)
            save_subtitles(text, audio_name)
            return f"Subtitles saved for: {audio_name}"

        def handle_phonemes(text):
            return auto_generate_phonemes(text, text_to_phonemes)

        transcribe_button.click(handle_transcription, audio_input, [transcribed_output, emotion_output])
        transcribe_button.click(handle_phonemes, transcribed_output, phoneme_output)
        clear_button.click(handle_clear, None, [transcribed_output, emotion_output, phoneme_output])
        save_button.click(handle_save, [audio_input, transcribed_output], None)

    return subtitle_ui
