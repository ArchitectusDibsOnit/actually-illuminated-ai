# song_structure_manager.py

import gradio as gr

# Predefined song structure tags
SONG_STRUCTURE_TAGS = [
    "[Intro]", "[Verse]", "[Chorus]", "[Bridge]", "[Hook]",
    "[Interlude]", "[Breakdown]", "[Build Up]", "[Bass Drop]",
    "[Big Finish]", "[Outro]", "[End]"
]

# Timeline storage
timeline = []

def add_event(event_tag, start_time, end_time):
    timeline.append({"tag": event_tag, "start": start_time, "end": end_time})
    return render_timeline(), render_timeline_chart()

def clear_timeline():
    timeline.clear()
    return render_timeline(), render_timeline_chart()

def render_timeline():
    if not timeline:
        return "Timeline is empty."
    return "\n".join(f"{e['tag']} from {e['start']}s to {e['end']}s" for e in timeline)

def render_timeline_chart():
    if not timeline:
        return "No chart to display."
    # ASCII bar chart: each second is one block
    return "\n".join(
        f"{e['tag']}: {'■' * max(1, int(e['end'] - e['start']))}"
        for e in timeline
    )

def song_structure_manager_interface():
    with gr.Blocks() as song_ui:
        gr.Markdown("## 🎵 Song Structure Manager")

        tag = gr.Dropdown(choices=SONG_STRUCTURE_TAGS, label="Select Tag")
        start = gr.Number(label="Start Time (s)", value=0)
        end = gr.Number(label="End Time (s)", value=10)

        add_btn = gr.Button("Add Event")
        clear_btn = gr.Button("Clear All")

        timeline_txt = gr.Textbox(label="Timeline", interactive=False, lines=8)
        chart_txt = gr.Textbox(label="Chart View", interactive=False, lines=8)

        add_btn.click(add_event, [tag, start, end], [timeline_txt, chart_txt])
        clear_btn.click(clear_timeline, None, [timeline_txt, chart_txt])

        # Initialize views
        timeline_txt.value = render_timeline()
        chart_txt.value = render_timeline_chart()

    return song_ui
