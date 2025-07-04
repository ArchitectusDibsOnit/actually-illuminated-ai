# voice_timeline_sync_engine.py

import gradio as gr
from song_structure_manager import timeline as song_timeline
from phoneme_onset_offset_editor import phoneme_timeline

# Voice Timeline Entries
voice_timeline = []

def add_voice_event(description, start_time, end_time):
    voice_timeline.append({"description": description, "start": start_time, "end": end_time})
    return render_voice_timeline()

def clear_voice_timeline():
    voice_timeline.clear()
    return render_voice_timeline()

def render_voice_timeline():
    if not voice_timeline:
        return "Voice timeline is empty."
    return "\n".join([f"{event['description']} from {event['start']}s to {event['end']}s" for event in voice_timeline])

def synchronize_voice_timeline():
    if not song_timeline or not phoneme_timeline:
        return "Error: Song timeline or phoneme timeline is empty."

    sync_results = []
    for structure_event in song_timeline:
        section_tag = structure_event['tag']
        section_start = structure_event['start']
        section_end = structure_event['end']

        # Find phonemes that occur within this section
        matching_phonemes = [
            p for p in phoneme_timeline if section_start <= p['onset'] <= section_end
        ]

        if matching_phonemes:
            phoneme_descriptions = ", ".join([f"{p['phoneme']}({p['onset']}s)" for p in matching_phonemes])
            sync_results.append(f"{section_tag} ({section_start}s - {section_end}s): {phoneme_descriptions}")
        else:
            sync_results.append(f"{section_tag} ({section_start}s - {section_end}s): [No phonemes detected]")

    return "\n".join(sync_results)

def voice_timeline_sync_interface():
    with gr.Blocks() as sync_ui:
        gr.Markdown("## 🔄 Voice Timeline Synchronizer and Phoneme Sync")

        with gr.Row():
            voice_description_input = gr.Textbox(label="Voice Description")
            start_input = gr.Number(label="Start Time (s)", value=0)
            end_input = gr.Number(label="End Time (s)", value=10)

        add_button = gr.Button("Add Voice Event")
        clear_button = gr.Button("Clear Voice Timeline")
        sync_button = gr.Button("Sync Song Structure with Phoneme Timeline")

        timeline_output = gr.Textbox(label="Voice Timeline / Phoneme Sync", lines=15, interactive=False)

        add_button.click(add_voice_event, [voice_description_input, start_input, end_input], timeline_output)
        clear_button.click(clear_voice_timeline, None, timeline_output)
        sync_button.click(synchronize_voice_timeline, None, timeline_output)

        timeline_output.value = render_voice_timeline()

    return sync_ui
