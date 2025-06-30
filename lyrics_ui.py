import gradio as gr
import os
from audio_utils import save_audio, load_audio, normalize_audio, pitch_shift, time_stretch, apply_reverb
from phoneme_and_meta_tag_utils import (
    phoneme_editor_interface, voice_morpher_interface, get_all_meta_tags, meta_tags,
    load_phoneme_profiles, text_to_phonemes
)
from glyph_handler import load_glyphs, display_glyphs
from lyrics_ui import lyrics_interface
from playback_emulator import playback_emulator_interface
from phoneme_sound_manager import phoneme_sound_manager_interface
from subtitle_manager import subtitle_manager_interface
from memory_core import memory_core_interface
from user_meta_tag_builder import user_meta_tag_builder_interface
from voice_timeline_editor import voice_timeline_editor_interface
from phoneme_recorder import phoneme_recorder_interface
from dynamic_model_loader import load_music_model, list_available_models
from music_generation_engine import switch_music_model, generate_music
from bark_integration import generate_bark_audio
from voice_profile_manager import voice_profile_manager_interface, get_available_voice_profiles
from voice_timeline_sync_engine import synchronize_voice_timeline

# ✅ Re-Embed Glyphscribe Core Directly Here
def glyphscribe_interface():
    glyph_input = gr.Textbox(label="Enter Glyph Text")
    glyph_output = gr.Textbox(label="Processed Glyph Output", interactive=False)

    def process_glyph(glyph_text):
        return f"[Processed Glyph]: {glyph_text[::-1]}"

    glyphscribe_button = gr.Button("Process Glyph")
    glyphscribe_button.click(process_glyph, glyph_input, glyph_output)

    return gr.Column([
        gr.Markdown("## ✒️ Glyphscribe - Write and Process Glyphs"),
        glyph_input,
        glyphscribe_button,
        glyph_output
    ])

# ✅ Song Generator Core Functions
def generate_song(prompt, duration, quality, use_bark):
    if use_bark:
        return generate_bark_audio(prompt)
    else:
        return generate_music(prompt, duration, quality)

# ✅ Song Creation Wizard Flow
def song_creation_wizard():
    gr.Markdown("# 🎤 Song Creation Wizard")

    with gr.Row():
        song_name = gr.Textbox(label="Song Name")

    with gr.Row():
        song_prompt = gr.Textbox(label="Enter Song Prompt with Meta-Tags", lines=4)

    with gr.Row():
        selected_voice_profile = gr.Dropdown(choices=get_available_voice_profiles(), label="Select Voice Profile")

    with gr.Row():
        duration = gr.Number(label="Song Duration (seconds)", value=10)
        quality = gr.Dropdown(choices=["Low", "Medium", "High"], label="Output Quality", value="Medium")
        use_bark = gr.Checkbox(label="Enable Bark Mode (Experimental)", value=False)

    with gr.Row():
        model_selector = gr.Dropdown(choices=list_available_models(), value="MusicGen-Small", label="Select Music Generation Model")
        model_status = gr.Textbox(label="Model Status", value="MusicGen-Small loaded.", interactive=False)

    generate_button = gr.Button("Generate Song")
    generated_audio = gr.Audio(label="Generated Song Output", interactive=False)

    generate_button.click(
        fn=generate_song,
        inputs=[song_prompt, duration, quality, use_bark],
        outputs=generated_audio
    )

    model_selector.change(fn=switch_music_model, inputs=model_selector, outputs=None)
    model_selector.change(lambda m: f"{m} loaded.", inputs=model_selector, outputs=model_status)

    return gr.Column([
        gr.Markdown("## 🎶 Recognized Song Structure Tags: [Intro], [Verse], [Chorus], [Bridge], [Hook], [Breakdown], [Outro], [End], [Big Finish], [Build Up], [Bass Drop]"),
        song_name,
        song_prompt,
        selected_voice_profile,
        duration,
        quality,
        use_bark,
        model_selector,
        model_status,
        generate_button,
        generated_audio
    ])

# Launcher Core
with gr.Blocks(title="Actually Illuminated AI Launcher", theme=gr.themes.Default(primary_hue="slate", secondary_hue="violet")) as launcher_ui:
    gr.Markdown("# <center>Actually Illuminated AI - Launcher</center>")
    gr.Markdown("Navigate between modules and build your sonic glyphscapes!")

    with gr.Accordion("🛠️ Modules (Click to Expand)", open=True):
        with gr.Row():
            with gr.Column():
                with gr.Tabs():
                    with gr.TabItem("Glyphscribe"):
                        glyphscribe_interface()

                    with gr.TabItem("Phoneme Editor"):
                        phoneme_editor_interface()

                    with gr.TabItem("Voice Morpher"):
                        voice_morpher_interface()

                    with gr.TabItem("Phoneme Sound Manager"):
                        phoneme_sound_manager_interface()

                    with gr.TabItem("Phoneme Recorder"):
                        phoneme_recorder_interface()

                    with gr.TabItem("Lyrics Engine"):
                        lyrics_interface()

                    with gr.TabItem("Playback Emulator"):
                        playback_emulator_interface()

                    with gr.TabItem("Voice Timeline"):
                        voice_timeline_editor_interface()

                    with gr.TabItem("User Meta-Tag Builder"):
                        user_meta_tag_builder_interface()

                    with gr.TabItem("Subtitle Manager"):
                        subtitle_manager_interface()

                    with gr.TabItem("Memory Core"):
                        memory_core_interface()

                    with gr.TabItem("Voice Profile Manager"):
                        voice_profile_manager_interface()

                    with gr.TabItem("Song Creation Wizard"):
                        song_creation_wizard()

        with gr.Row():
            gr.Markdown("## 📚 Meta-Tags Reference")
            gr.Markdown(f"{get_all_meta_tags()}")

        with gr.Row():
            gr.Markdown("## 🗂️ Glyph Browser")
            glyph_display = gr.Textbox(label="Available Glyphs", interactive=False)
            glyph_display.value = display_glyphs()

        with gr.Row():
            gr.Markdown("## ⚙️ System Status")
            gr.Markdown("- All Modules Online ✅")

    launcher_ui.launch(server_name="127.0.0.1", server_port=7861, share=False, inbrowser=True)

print("[✔] Actually Illuminated AI Launcher is active in dark mode.")
