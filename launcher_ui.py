# launcher_ui.py (MAXED OUT GlyphClippy: Animated, TTS, Suggestion-Aware, Emotive AI Assistant)

import gradio as gr
import os
import pyttsx3
import random

from audio_utils import save_audio, load_audio, normalize_audio, pitch_shift, time_stretch, apply_reverb
from phoneme_and_meta_tag_utils import get_all_meta_tags, meta_tags, get_tags
from glyph_handler import display_glyphs
from playback_emulator import playback_emulator_interface
from phoneme_sound_manager import phoneme_sound_manager_interface
from subtitle_manager import subtitle_interface
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

# Voice setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
clippy_voices = {
    "Narrator": voices[0].id if voices else None,
    "Meme Lord": voices[-1].id if voices else None,
    "Default": None
}
def speak(text, voice_mode="Default"):
    try:
        if clippy_voices.get(voice_mode):
            engine.setProperty('voice', clippy_voices[voice_mode])
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS ERROR]: {e}")

# Preemptive tab suggestion logic
context_suggestions = {
    "Song Creation Wizard": "Want help building a meta-tag stack?",
    "Voice Profile Manager": "Need a walkthrough on voice cloning?",
    "Meta-Tag Builder": "Want to auto-generate a tag chain from lyrics?",
    "Lyrics Tool": "Need cipher tricks or hidden acrostics?",
    "Benchmark & Stats": "Curious how to optimize your latency or GPU usage?"
}

# 🔥 Floating Clippy Modal with Emotes, Voice, Suggestions

def floating_glyphclippy_box():
    with gr.Box(elem_id="glyph-clippy-box"):
        clippy_img = gr.Image(value="assets/glyphclippy_idle.png", show_label=False, interactive=True)

    with gr.Box(visible=False, elem_id="clippy-modal") as clippy_modal:
        gr.Markdown('<span id="clippy-close">\u2716</span>', elem_id=None)
        active_tab = gr.Textbox(value="Song Creation Wizard", visible=False)
        voice_select = gr.Radio(["Default", "Narrator", "Meme Lord"], value="Default", label="🗣️ Voice Mode")

        clippy_chat = gr.Textbox(placeholder="Ask GlyphClippy something...", label="Chat")
        clippy_button = gr.Button("Ask")
        clippy_output = gr.Textbox(label="Clippy Responds", lines=4, interactive=False)
        clippy_memory = gr.Textbox(label="Memory", lines=3, interactive=False)
        clear_mem = gr.Button("Clear Memory")
        suggestion_button = gr.Button("Suggest Prompt from Current Tab 🧠")

        def clippy_talk(input_text, context, mode):
            reply = GlyphClippy.chat(f"[{context}] {input_text}")
            memory = GlyphClippy.get_memory()
            speak(reply, mode)
            return reply, memory

        def suggest_from_tab(context):
            suggestion = context_suggestions.get(context, "I'm not sure what to suggest here, but ask me anything!")
            return suggestion

        clippy_button.click(clippy_talk, [clippy_chat, active_tab, voice_select], [clippy_output, clippy_memory])
        suggestion_button.click(suggest_from_tab, active_tab, clippy_output)
        clear_mem.click(lambda: GlyphClippy.clear_memory() or ("Memory cleared.", ""), None, [clippy_output, clippy_memory])

    gr.HTML("""
    <script>
    const clippy = document.getElementById("glyph-clippy-box");
    const modal = document.getElementById("clippy-modal");
    const closeBtn = document.getElementById("clippy-close");

    clippy.addEventListener("click", () => {
        modal.classList.toggle("show");
    });

    closeBtn.addEventListener("click", () => {
        modal.classList.remove("show");
    });

    const observer = new MutationObserver(() => {
        const activeTab = document.querySelector('.svelte-tabitem span')?.innerText;
        const input = document.querySelector('input[type="text"][value="Song Creation Wizard"]');
        if (input && activeTab && input.value !== activeTab) {
            input.value = activeTab;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """)

# ✅ MAIN LAUNCHER
with gr.Blocks(title="Actually Illuminated AI Launcher",
               theme=gr.themes.Default(primary_hue="slate", secondary_hue="violet"),
               css="static/style.css") as launcher:

    gr.Markdown("# <center>🎧 Actually Illuminated AI Launcher</center>")
    gr.Markdown("A complete local music+voice AI studio.")

    with gr.Tabs():
        with gr.TabItem("🎼 Song Creation Wizard"): song_creation_wizard()
        with gr.TabItem("🎙️ Voice Profile Manager"): voice_profile_manager_interface()
        with gr.TabItem("🎹 Voice Timeline Sync"): voice_timeline_sync_interface()
        with gr.TabItem("🧬 Phoneme Editor"): phoneme_editor_interface()
        with gr.TabItem("🔊 Playback Emulator"): playback_emulator_interface()
        with gr.TabItem("🎮 Phoneme Sound Manager"): phoneme_sound_manager_interface()
        with gr.TabItem("🧠 Memory Core"): memory_core_interface()
        with gr.TabItem("📜 Subtitles & Timestamps"): subtitle_interface()
        with gr.TabItem("🎶 Meta-Tag Soundboard"): meta_tag_soundboard_ui()
        with gr.TabItem("🛠️ Meta-Tag Builder"): user_meta_tag_builder_interface()
        with gr.TabItem("🎼 Multi-Voice Mixer"): multi_voice_mixer_interface()
        with gr.TabItem("🎙️ Phoneme Recorder"): phoneme_recorder_interface()
        with gr.TabItem("🔄 Phoneme Mixer"): phoneme_replacement_interface()
        with gr.TabItem("🧪 Meta Preview"): meta_tag_preview_ui()
        with gr.TabItem("🗌 Song Structure Manager"): song_structure_manager_interface()
        with gr.TabItem("📝 Lyrics Tool"): lyrics_interface()
        with gr.TabItem("🧠 Benchmark & Stats"): system_performance_tab()
        with gr.TabItem("✒️ Glyphscribe"): glyphscribe_interface()
        with gr.TabItem("🤖 GlyphClippy Assistant"): glyphclippy_interface()

    with gr.Accordion("🔍 Meta-Tags & Glyph Overview", open=False):
        with gr.Row():
            gr.Markdown("### Meta-Tags")
            gr.Markdown(get_all_meta_tags())
        with gr.Row():
            gr.Markdown("### Glyphs")
            glyph_box = gr.Textbox(label="Available Glyphs", interactive=False)
            glyph_box.value = display_glyphs()

    floating_glyphclippy_box()

    launcher.launch(server_name="127.0.0.1", server_port=7861, share=False, inbrowser=True)

print("[✔] Actually Illuminated AI Launcher with GlyphClippy: Now Talking, Thinking, and Scheming.")
