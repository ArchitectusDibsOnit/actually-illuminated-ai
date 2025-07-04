# launcher_ui.py (Visual Timeline Viewer Integrated)

import gradio as gr
import os

from audio_utils import save_audio, load_audio, normalize_audio, pitch_shift, time_stretch, apply_reverb
from phoneme_and_meta_tag_utils import (
    phoneme_editor_interface, voice_morpher_interface, get_all_meta_tags, meta_tags,
    load_phoneme_profiles, text_to_phonemes, get_tags
)
from glyph_handler import load_glyphs, display_glyphs
from playback_emulator import playback_emulator_interface
from phoneme_sound_manager import phoneme_sound_manager_interface
from subtitle_manager import transcribe_audio, save_subtitles, get_subtitles, auto_generate_phonemes
from subtitle_ui import subtitle_interface
from memory_core import memory_core_interface
from user_meta_tag_builder import user_meta_tag_builder_interface
from voice_timeline_editor import voice_timeline_editor_interface
from phoneme_recorder import phoneme_recorder_interface
from dynamic_model_loader import load_music_model, list_available_models
from music_generation_engine import switch_music_model, generate_music
from frame_slicer import frame_sliced_generate
from system_performance import recommend_max_frame, estimate_eta, system_summary, benchmark_system_speed
from bark_integration import generate_bark_audio
from voice_profile_manager import voice_profile_manager_interface, get_available_voice_profiles
from voice_timeline_sync_engine import voice_timeline_sync_interface
from phoneme_mixer_engine import phoneme_replacement_interface
from multi_voice_mixer import multi_voice_mixer_interface
from meta_tag_soundboard import meta_tag_soundboard_ui
from meta_tag_preview import meta_tag_preview_ui
from lyrics_ui import lyrics_interface
from song_structure_manager import song_structure_manager_interface
from visual_timeline_viewer import visual_timeline_viewer_interface

# ✅ System Performance Tab
def system_performance_tab():
    with gr.Blocks() as system_ui:
        gr.Markdown("## 🖥️ System Performance & Benchmark")
        system_info = gr.Textbox(label="System Summary", value=system_summary(), interactive=False)
        benchmark_output = gr.Textbox(label="Benchmark Result", interactive=False)
        benchmark_button = gr.Button("Run Performance Benchmark")

        benchmark_button.click(fn=benchmark_system_speed, inputs=None, outputs=benchmark_output)

    return system_ui

# ✅ Song Creation Wizard
def song_creation_wizard():
    with gr.Blocks() as wizard_ui:
        gr.Markdown("# 🎤 Song Creation Wizard")

        mode_selector = gr.Radio(choices=["Simple", "Advanced"], label="Select Mode", value="Simple")

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
            model_selector = gr.Dropdown(choices=list_available_models(), value="facebook/musicgen-small", label="Select Music Generation Model")
            model_status = gr.Textbox(label="Model Status", value="facebook/musicgen-small loaded.", interactive=False)

        with gr.Row():
            style_tags = gr.Dropdown(choices=get_tags("genres") + get_tags("styles"), multiselect=True, label="Select Style/Genre Tags", interactive=True)
            voice_tags = gr.Dropdown(choices=get_tags("voices"), multiselect=True, label="Select Vocal/Character Tags", interactive=True)
            music_sfx_tags = gr.Dropdown(choices=get_tags("instruments") + get_tags("sfx"), multiselect=True, label="Select Music/SFX/Glyph Tags", interactive=True)

        slice_notice = gr.Textbox(label="Frame Slicer Status", interactive=False)
        generate_button = gr.Button("Generate Song")
        generated_audio = gr.Audio(label="Generated Song Output", interactive=False)

        def build_and_generate(prompt, duration, quality, use_bark, style, voice, sfx):
            tag_string = " ".join(style + voice + sfx)
            full_prompt = f"{tag_string}\n{prompt}"
            recommended_max = recommend_max_frame()

            if duration > recommended_max:
                eta = estimate_eta(duration, recommended_max)
                slice_notice.value = f"[⚙️] Auto frame-slicing enabled. ETA: {eta}s."
                return frame_sliced_generate(full_prompt, duration, quality)
            else:
                slice_notice.value = f"[✔] No slicing required. Generating normally."
                return generate_music(full_prompt, duration, quality)

        generate_button.click(
            fn=build_and_generate,
            inputs=[song_prompt, duration, quality, use_bark, style_tags, voice_tags, music_sfx_tags],
            outputs=generated_audio
        )

        model_selector.change(fn=switch_music_model, inputs=model_selector, outputs=None)
        model_selector.change(lambda m: f"{m} loaded.", inputs=model_selector, outputs=model_status)

    return wizard_ui

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

                    with gr.TabItem("Playback Emulator"):
                        playback_emulator_interface()

                    with gr.TabItem("Voice Timeline"):
                        voice_timeline_editor_interface()

                    with gr.TabItem("Voice Timeline Sync"):
                        voice_timeline_sync_interface()

                    with gr.TabItem("User Meta-Tag Builder"):
                        user_meta_tag_builder_interface()

                    with gr.TabItem("Subtitle Manager"):
                        subtitle_interface()

                    with gr.TabItem("Memory Core"):
                        memory_core_interface()

                    with gr.TabItem("Voice Profile Manager"):
                        voice_profile_manager_interface()

                    with gr.TabItem("Phoneme Mixer"):
                        phoneme_replacement_interface()

                    with gr.TabItem("Multi-Voice Mixer"):
                        multi_voice_mixer_interface()

                    with gr.TabItem("Meta-Tag Soundboard"):
                        meta_tag_soundboard_ui()

                    with gr.TabItem("Meta-Tag Preview"):
                        meta_tag_preview_ui()

                    with gr.TabItem("Song Structure Manager"):
                        song_structure_manager_interface()

                    with gr.TabItem("Lyrics Parser"):
                        lyrics_interface()

                    with gr.TabItem("Song Creation Wizard"):
                        song_creation_wizard()

                    with gr.TabItem("Visual Timeline Viewer"):
                        visual_timeline_viewer_interface()

                    with gr.TabItem("System Performance"):
                        system_performance_tab()

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
