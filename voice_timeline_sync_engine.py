# voice_timeline_sync_engine.py

import gradio as gr
from song_structure_manager import timeline as song_timeline

voice_timeline = []

def add_voice_event(desc, start, end):
    voice_timeline.append({"description": desc, "start": start, "end": end})
    return render_voice(), render_voice_chart()

def clear_voice_timeline():
    voice_timeline.clear()
    return render_voice(), render_voice_chart()

def render_voice():
    if not voice_timeline:
        return "Voice timeline is empty."
    return "\n".join(f"{e['description']} from {e['start']}s to {e['end']}s" for e in voice_timeline)

def render_voice_chart():
    if not voice_timeline:
        return "No chart to display."
    return "\n".join(
        f"{e['description']}: {'■' * max(1, int(e['end'] - e['start']))}"
        for e in voice_timeline
    )

def synchronize_voice_timeline():
    voice_timeline.clear()
    for e in song_timeline:
        voice_timeline.append({
            "description": f"Voice for {e['tag']}",
            "start": e['start'],
            "end": e['end']
        })
    return render_voice(), render_voice_chart()

def voice_timeline_sync_interface():
    with gr.Blocks() as ui:
        gr.Markdown("## 🔄 Voice Timeline Synchronizer")

        desc = gr.Textbox(label="Description")
        start = gr.Number(label="Start Time (s)", value=0)
        end = gr.Number(label="End Time (s)", value=10)

        add_btn = gr.Button("Add Voice Event")
        clear_btn = gr.Button("Clear Voice Timeline")
        sync_btn = gr.Button("Sync with Structure")

        timeline_txt = gr.Textbox(label="Voice Timeline", interactive=False, lines=8)
        chart_txt = gr.Textbox(label="Voice Chart View", interactive=False, lines=8)

        add_btn.click(add_voice_event, [desc, start, end], [timeline_txt, chart_txt])
        clear_btn.click(clear_voice_timeline, None, [timeline_txt, chart_txt])
        sync_btn.click(synchronize_voice_timeline, None, [timeline_txt, chart_txt])

        timeline_txt.value = render_voice()
        chart_txt.value = render_voice_chart()

    return ui
