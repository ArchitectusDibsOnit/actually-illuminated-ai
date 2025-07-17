# subtitle_ui.py (Enhanced UI)

import os
import gradio as gr
from subtitle_manager import transcribe_audio
from emotional_phonemizer import analyze_text_for_phonemes_and_emotion, GLYPH_ANIMATIONS
from clippy_tts_speaker import speak_text_with_emotion


def subtitle_interface():
    with gr.Blocks() as subtitle_ui:
        gr.Markdown("## 📝 Subtitle Manager + Emotion Detection + Clippy TTS + Phonemizer")

        with gr.Row():
            audio_input = gr.Audio(type="filepath", label="Upload Audio File")

        transcribed_output = gr.Textbox(label="Transcribed Subtitles", lines=6)
        emotion_output = gr.Textbox(label="Detected Emotion", lines=1, interactive=False)
        glyph_display = gr.Textbox(label="Emotion Glyph", lines=1, interactive=False)
        phoneme_output = gr.Textbox(label="Generated Phonemes", lines=4, interactive=False)
        tags_output = gr.Textbox(label="Meta Tags", lines=2, interactive=False)

        with gr.Row():
            transcribe_button = gr.Button("Transcribe & Analyze")
            clear_button = gr.Button("Clear")
            speak_button = gr.Button("🔊 Clippy Speak")

        def handle_transcription(audio_path):
            text, _ = transcribe_audio(audio_path)
            analysis = analyze_text_for_phonemes_and_emotion(text)
            animated_glyph = GLYPH_ANIMATIONS.get(analysis["glyph"], analysis["glyph"])
            return (
                text,
                analysis["emotion"].capitalize(),
                animated_glyph,
                analysis["phonemes"],
                ", ".join(analysis["tags"])
            )

        def handle_clear():
            return "", "", "", "", ""

        def handle_clippy_speak(text, emotion):
            speak_text_with_emotion(text, emotion)
            return "Speaking triggered."

        transcribe_button.click(
            handle_transcription,
            audio_input,
            [transcribed_output, emotion_output, glyph_display, phoneme_output, tags_output]
        )
        clear_button.click(handle_clear, None, [transcribed_output, emotion_output, glyph_display, phoneme_output, tags_output])
        speak_button.click(handle_clippy_speak, [transcribed_output, emotion_output], None)

    return subtitle_ui
