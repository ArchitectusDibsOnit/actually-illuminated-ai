# phoneme_onset_offset_editor.py (Upgraded with Timeline Sync and Profiles)

import gradio as gr
from song_structure_manager import SONG_STRUCTURE_TAGS
from voice_profile_manager import get_available_voice_profiles

# In-memory phoneme timeline storage
phoneme_timeline = []

def add_phoneme_event(phoneme, onset, offset, song_section, voice_profile):
    if onset >= offset:
        return display_phoneme_timeline(), "⛔ Onset must be before Offset."
    
    phoneme_timeline.append({
        "phoneme": phoneme,
        "onset": onset,
        "offset": offset,
        "section": song_section,
        "voice": voice_profile
    })
    phoneme_timeline.sort(key=lambda x: x['onset'])  # Auto-sort by onset
    return display_phoneme_timeline(), "✅ Phoneme event added."

def clear_phoneme_timeline():
    phoneme_timeline.clear()
    return display_phoneme_timeline(), "🧹 Phoneme timeline cleared."

def display_phoneme_timeline():
    if not phoneme_timeline:
        return "Phoneme timeline is empty."
    return "\n".join([
        f"[{event['voice']}] {event['phoneme']} from {event['onset']}s to {event['offset']}s in {event['section']}"
        for event in phoneme_timeline
    ])

def export_phoneme_timeline():
    return phoneme_timeline  # For voice_timeline_sync_engine

def phoneme_onset_offset_editor_interface():
    with gr.Blocks() as phoneme_editor_ui:
        gr.Markdown("## 🕰️ Phoneme Onset/Offset Editor with Timeline Sync")

        with gr.Row():
            phoneme_input = gr.Textbox(label="Phoneme")
            onset_input = gr.Number(label="Onset Time (s)", value=0)
            offset_input = gr.Number(label="Offset Time (s)", value=1)

        with gr.Row():
            song_section_selector = gr.Dropdown(choices=SONG_STRUCTURE_TAGS, label="Assign to Song Section")
            voice_profile_selector = gr.Dropdown(choices=get_available_voice_profiles(), label="Select Voice Profile")

        add_button = gr.Button("Add Phoneme Event")
        clear_button = gr.Button("Clear Phoneme Timeline")

        phoneme_timeline_display = gr.Textbox(label="Phoneme Timeline", lines=12, interactive=False)
        status_display = gr.Textbox(label="Status", interactive=False)

        add_button.click(
            fn=add_phoneme_event,
            inputs=[phoneme_input, onset_input, offset_input, song_section_selector, voice_profile_selector],
            outputs=[phoneme_timeline_display, status_display]
        )

        clear_button.click(
            fn=clear_phoneme_timeline,
            inputs=None,
            outputs=[phoneme_timeline_display, status_display]
        )

        phoneme_timeline_display.value = display_phoneme_timeline()

    return phoneme_editor_ui

# This function will be used by the sync engine
def get_phoneme_timeline():
    return phoneme_timeline
