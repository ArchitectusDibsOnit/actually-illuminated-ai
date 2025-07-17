# subtitle_ui.py (Emotion Glyph + Phoneme Display UI + Clippy TTS)

import os
import gradio as gr
from subtitle_manager import transcribe_audio, save_subtitles, get_subtitles
from emotional_phonemizer import analyze_text_for_phonemes_and_emotion, GLYPH_ANIMATIONS
from clippy_tts import speak_with_emotion


def subtitle_interface():
    with gr.Blocks() as subtitle_ui:
        gr.Markdown("## 🎙️ Subtitle Manager + Emotion + Phoneme Magic + Clippy TTS")

        with gr.Row():
            audio_input = gr.Audio(type="filepath", label="🎧 Upload Audio File")

        transcribed_output = gr.Textbox(label="📝 Transcribed Subtitles", lines=6)
        emotion_output = gr.Textbox(label="💥 Dominant Emotion", lines=1, interactive=False)
        phoneme_output = gr.Textbox(label="🔤 Generated Phonemes", lines=6, interactive=False)
        tag_output = gr.Textbox(label="🏷️ Detected Meta-Tags", lines=2, interactive=False)

        with gr.Row():
            transcribe_button = gr.Button("🧠 Analyze Audio")
            clear_button = gr.Button("🧹 Clear")
            save_button = gr.Button("💾 Save Results")

        def handle_transcription(audio_path):
            text, segments = transcribe_audio(audio_path)
            emotion_counts = {}
            all_phonemes = []
            all_tags = set()

            for seg in segments:
                enriched = analyze_text_for_phonemes_and_emotion(seg['text'])
                seg['emotion'] = enriched['emotion']
                seg['glyph'] = GLYPH_ANIMATIONS.get(enriched['glyph'], enriched['glyph'])
                seg['phonemes'] = enriched['phonemes']
                seg['tags'] = enriched['tags']

                all_phonemes.append(f"[{seg['glyph']}] {enriched['phonemes']}")
                all_tags.update(enriched['tags'])
                emotion_counts[enriched['emotion']] = emotion_counts.get(enriched['emotion'], 0) + 1

                # 🎤 Let Clippy speak with emotion!
                speak_with_emotion(seg['text'], enriched['emotion'])

            dominant = max(emotion_counts.items(), key=lambda x: x[1])[0]
            glyph = GLYPH_ANIMATIONS.get(GLYPH_ANIMATIONS.get(dominant, '😐'), '😐')

            return text, f"{glyph} {dominant}", "\n".join(all_phonemes), ", ".join(sorted(all_tags))

        def handle_clear():
            return "", "", "", ""

        def handle_save(audio_path, text):
            audio_name = os.path.basename(audio_path)
            save_subtitles(text, audio_name)
            return f"✅ Subtitles saved for: {audio_name}"

        transcribe_button.click(handle_transcription, audio_input, [transcribed_output, emotion_output, phoneme_output, tag_output])
        clear_button.click(handle_clear, None, [transcribed_output, emotion_output, phoneme_output, tag_output])
        save_button.click(handle_save, [audio_input, transcribed_output], None)

    return subtitle_ui
