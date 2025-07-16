# launcher_ui.py (Floating GlyphClippy + Tab Access + TTS Selector)

import gradio as gr
import os

from audio_utils import save_audio, load_audio, normalize_audio, pitch_shift, time_stretch, apply_reverb
from phoneme_and_meta_tag_utils import get_all_meta_tags, meta_tags, get_tags
from glyph_handler import display_glyphs
from playback_emulator import playback_emulator_interface
from phoneme_sound_manager import phoneme_sound_manager_interface
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
from voice_profile_manager import voice_profile_manager_interface, get_available_voice_profiles, load_voice_profiles
from voice_timeline_sync_engine import voice_timeline_sync_interface
from phoneme_mixer_engine import phoneme_replacement_interface
from multi_voice_mixer import multi_voice_mixer_interface
from meta_tag_soundboard import meta_tag_soundboard_ui
from meta_tag_preview import meta_tag_preview_ui
from lyrics_ui import lyrics_interface
from song_structure_manager import song_structure_manager_interface
from async_utils import async_wrapper
from phoneme_editor import phoneme_editor_interface
from timeline_visualizer import timeline_visualizer_interface
from glyphclippy_engine import GlyphClippy
from tts_selector_ui import clippy_tts_selector_ui

# 💬 GlyphClippy Floating Assistant Panel (for tab view)
def glyphclippy_interface():
    with gr.Blocks() as clippy_ui:
        gr.Markdown("## 🤖 GlyphClippy Assistant")

        with gr.Row():
            clippy_chat_input = gr.Textbox(placeholder="Ask anything about this system...", label="Talk to GlyphClippy")
            clippy_button = gr.Button("Ask")

        clippy_response_output = gr.Textbox(label="Clippy's Response", lines=4, interactive=False)
        clippy_memory_output = gr.Textbox(label="Clippy Memory", lines=5, interactive=False)
        clear_button = gr.Button("Clear Memory")

        def handle_chat(message):
            reply = GlyphClippy.chat(message)
            memory = GlyphClippy.get_memory()
            return reply, memory

        clippy_button.click(handle_chat, clippy_chat_input, [clippy_response_output, clippy_memory_output])
        clear_button.click(lambda: GlyphClippy.clear_memory() or ("Memory cleared.", ""), None, [clippy_response_output, clippy_memory_output])

        gr.Markdown("---")
        gr.Markdown("### 🔊 TTS + Emotion Controls")
        clippy_tts_selector_ui()

    return clippy_ui

# ✅ Floating GlyphClippy Element Across UI
def floating_glyphclippy_box():
    with gr.Box(elem_id="glyph-clippy-box"):
        with gr.Column():
            gr.Image(value="assets/glyphclippy_idle.png", show_label=False, interactive=False)
            gr.Markdown("**Need help?**", elem_id="glyph-clippy-text")

# ✅ MAIN LAUNCHER
with gr.Blocks(title="Actually Illuminated AI Launcher",
               theme=gr.themes.Default(primary_hue="slate", secondary_hue="violet"),
               css="static/style.css") as launcher:

    gr.Markdown("# <center>🎛️ Actually Illuminated AI Launcher</center>")
    gr.Markdown("A complete local music+voice AI studio.")

    with gr.Tabs():
        with gr.TabItem("🎼 Song Creation Wizard"): song_creation_wizard()
        with gr.TabItem("🎙️ Voice Profile Manager"): voice_profile_manager_interface()
        with gr.TabItem("🎚️ Voice Timeline Sync"): voice_timeline_sync_interface()
        with gr.TabItem("🧬 Phoneme Editor"): phoneme_editor_interface()
        with gr.TabItem("🔉 Playback Emulator"): playback_emulator_interface()
        with gr.TabItem("🎛️ Phoneme Sound Manager"): phoneme_sound_manager_interface()
        with gr.TabItem("🧠 Memory Core"): memory_core_interface()
        with gr.TabItem("📜 Subtitles & Timestamps"): subtitle_interface()
        with gr.TabItem("🎶 Meta-Tag Soundboard"): meta_tag_soundboard_ui()
        with gr.TabItem("🛠️ Meta-Tag Builder"): user_meta_tag_builder_interface()
        with gr.TabItem("🎹 Multi-Voice Mixer"): multi_voice_mixer_interface()
        with gr.TabItem("🎙️ Phoneme Recorder"): phoneme_recorder_interface()
        with gr.TabItem("🔄 Phoneme Mixer"): phoneme_replacement_interface()
        with gr.TabItem("🧪 Meta Preview"): meta_tag_preview_ui()
        with gr.TabItem("🗺️ Song Structure Manager"): song_structure_manager_interface()
        with gr.TabItem("📝 Lyrics Tool"): lyrics_interface()
        with gr.TabItem("🧠 Benchmark & Stats"): system_performance_tab()
        with gr.TabItem("✒️ Glyphscribe"): glyphscribe_interface()
        with gr.TabItem("📊 Timeline Visualizer"): timeline_visualizer_interface()
        with gr.TabItem("🤖 GlyphClippy Assistant"): glyphclippy_interface()

    with gr.Accordion("🔍 Meta-Tags & Glyph Overview", open=False):
        with gr.Row():
            gr.Markdown("### Meta-Tags")
            gr.Markdown(get_all_meta_tags())
        with gr.Row():
            gr.Markdown("### Glyphs")
            glyph_box = gr.Textbox(label="Available Glyphs", interactive=False)
            glyph_box.value = display_glyphs()

    # Add floating assistant across all tabs
    floating_glyphclippy_box()

    launcher.launch(server_name="127.0.0.1", server_port=7861, share=False, inbrowser=True)

print("[✔] Actually Illuminated AI Launcher with Floating GlyphClippy + TTS Mode Selector is running.")
