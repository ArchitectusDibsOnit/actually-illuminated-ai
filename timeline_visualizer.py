# timeline_visualizer.py (Emotion Overlay + Clippy Trigger Hooks)

import gradio as gr
import os
import json
from glyphclippy_engine import set_clippy_state  # New import to trigger Clippy

SUBTITLE_DIR = "subtitles"

emotion_colors = {
    "Happy": "#FFD700",
    "Sad": "#6495ED",
    "Angry": "#FF4500",
    "Surprise": "#DA70D6",
    "Fear": "#A52A2A",
    "Disgust": "#556B2F",
    "Neutral": "#D3D3D3"
}

clippy_hooks = {
    "Happy": "smile",
    "Sad": "droop",
    "Angry": "rage",
    "Surprise": "jump",
    "Fear": "shiver",
    "Disgust": "gag",
    "Neutral": "idle"
}

def timeline_visualizer_interface():
    with gr.Blocks() as timeline_ui:
        gr.Markdown("## 📊 Emotion Timeline Visualizer + Clippy Sync")

        json_input = gr.File(label="📥 Upload Segment JSON", file_types=[".json"])
        timeline_output = gr.HTML(label="🎞️ Timeline Display")
        clippy_trigger_output = gr.Textbox(label="🧠 Clippy Reacts As", interactive=False)

        def render_emotion_timeline(json_file):
            if not json_file:
                return "No file uploaded.", ""
            with open(json_file.name, "r", encoding="utf-8") as f:
                segments = json.load(f)

            html = ["<div style='display:flex;gap:4px'>"]
            clippy_states = set()

            for seg in segments:
                emo = seg.get("emotion", "Neutral")
                color = emotion_colors.get(emo, "#CCC")
                tooltip = f"{seg['start_time']}s–{seg['end_time']}s: {emo}"
                html.append(f"<div title='{tooltip}' style='flex:1;height:20px;background:{color};border-radius:3px'></div>")
                clippy_state = clippy_hooks.get(emo, "idle")
                clippy_states.add(clippy_state)
                set_clippy_state(clippy_state)  # Trigger Clippy visual change

            html.append("</div>")
            return "\n".join(html), ", ".join(sorted(clippy_states))

        json_input.change(render_emotion_timeline, json_input, [timeline_output, clippy_trigger_output])

    return timeline_ui
