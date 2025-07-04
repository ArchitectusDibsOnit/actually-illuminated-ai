# 🎼 song_structure_manager.py

import gradio as gr

# Predefined song structure tags
SONG_STRUCTURE_TAGS = [
    "[Intro]", "[Verse]", "[Chorus]", "[Bridge]", "[Hook]", "[Interlude]", "[Breakdown]",
    "[Build Up]", "[Bass Drop]", "[Big Finish]", "[Outro]", "[End]"
]

# Simple timeline event storage
timeline = []


def add_event(event_tag, start_time, end_time):
    timeline.append({"tag": event_tag, "start": start_time, "end": end_time})
    return display_timeline()



def clear_timeline():
    timeline.clear()
    return display_timeline()



def display_timeline():
    if not timeline:
        return "Timeline is empty."
    return "\n".join([f"{event['tag']} from {event['start']}s to {event['end']}s" for event in timeline])



def song_structure_manager_interface():
    with gr.Blocks() as song_structure_ui:
        gr.Markdown("## 🎵 Song Structure Manager - Tag & Timeline Editor")

        with gr.Row():
            tag_selector = gr.Dropdown(choices=SONG_STRUCTURE_TAGS, label="Select Song Section Tag", interactive=True)
            custom_tag_input = gr.Textbox(label="Or Enter Custom Tag")
            start_input = gr.Number(label="Start Time (s)", value=0)
            end_input = gr.Number(label="End Time (s)", value=10)

        add_button = gr.Button("Add Event to Timeline")
        clear_button = gr.Button("Clear Timeline")

        timeline_display = gr.Textbox(label="Song Timeline", lines=10, interactive=False)

        def add_timeline_event(tag, custom_tag, start, end):
            final_tag = custom_tag.strip() if custom_tag.strip() else tag
            if final_tag not in SONG_STRUCTURE_TAGS:
                SONG_STRUCTURE_TAGS.append(final_tag)
            return add_event(final_tag, start, end)

        add_button.click(add_timeline_event, [tag_selector, custom_tag_input, start_input, end_input], timeline_display)
        clear_button.click(lambda: clear_timeline(), None, timeline_display)

        timeline_display.value = display_timeline()

    return song_structure_ui


# 🔥 Next Step: Build the Voice Onset/Offset Editor + Integration with this timeline
