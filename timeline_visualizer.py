# timeline_visualizer.py

import gradio as gr
from song_structure_manager import timeline as song_timeline
from voice_timeline_sync_engine import voice_timeline

def build_text_timeline():
    if not song_timeline and not voice_timeline:
        return "🔫 Nothing to visualize yet."

    lines = ["## 🎼 Song Timeline Overview:"]
    for event in song_timeline:
        lines.append(f"[SONG] {event['tag']} → {event['start']}s to {event['end']}s")

    lines.append("\n## 🎹 Voice Timeline Overview:")
    for event in voice_timeline:
        lines.append(f"[VOICE] {event['description']} → {event['start']}s to {event['end']}s")

    return "\n".join(lines)

def timeline_visualizer_interface():
    with gr.Blocks() as timeline_ui:
        gr.Markdown("## 🧭 Timeline Visualizer")
        output = gr.Textbox(lines=20, label="Timeline", interactive=False)
        refresh = gr.Button("🔄 Refresh")

        refresh.click(lambda: build_text_timeline(), None, output)
        output.value = build_text_timeline()

    return timeline_ui
