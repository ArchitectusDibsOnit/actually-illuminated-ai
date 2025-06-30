# subtitle_ui.py

import gradio as gr
from subtitle_manager import transcribe_audio, save_subtitles, get_subtitles, auto_generate_phonemes
from phoneme_and_meta_tag_utils import text_to_phonemes

def subtitle_interface():
    with gr.Blocks() as subtitle_ui:
        gr.Markdown("## 📝 Subtitle Manager + Phoneme Generator")

        with gr.Row():
            audio_input = gr.Audio(source="upload", type="filepath", label="Upload Audio File")

        transcribed_output = gr.Textbox(label="Transcribed Subtitles", lines=6)

        with gr.Row():
            transcribe_button = gr.Button("Transcribe Audio")
            clear_button = gr.Button("Clear")

        phoneme_output = gr.Textbox(label="Auto-Generated Phonemes", lines=6, interactive=False)

        with gr.Row():
            save_button = gr.Button("Save Subtitles and Phonemes")

        def handle_transcription(audio_path):
            text, _ = transcribe_audio(audio_path)
            return text

        def handle_clear():
            return "", ""

        def handle_save(audio_path, text):
            audio_name = os.path.basename(audio_path)
            save_subtitles(text, audio_name)
            return f"Subtitles saved for: {audio_name}"

        def handle_phonemes(text):
            return auto_generate_phonemes(text, text_to_phonemes)

        transcribe_button.click(handle_transcription, audio_input, transcribed_output)
        transcribe_button.click(handle_phonemes, transcribed_output, phoneme_output)
        clear_button.click(handle_clear, None, [transcribed_output, phoneme_output])
        save_button.click(handle_save, [audio_input, transcribed_output], None)

    return subtitle_ui
