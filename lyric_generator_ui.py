# lyric_generator_ui.py (Gradio UI for Lyric Generator + Style Presets + Guided Mode)

import gradio as gr
from lyric_generator import generate_lyrics_from_tags, generate_lyrics_from_description
from prompt_assistant import get_preset_styles, apply_preset_style, guided_tag_wizard

with gr.Blocks() as lyric_ui:
    gr.Markdown("## 🎼 AI Lyric Generator (Suno-Style) with Meta-Tag Magic")

    with gr.Tabs():

        with gr.TabItem("🎨 Preset Style"):
            with gr.Row():
                preset_dropdown = gr.Dropdown(label="Choose a Style Preset", choices=get_preset_styles())
                apply_preset_button = gr.Button("🎯 Load Tags")
            preset_tags_box = gr.Textbox(label="Generated Tags", interactive=False)
            preset_generate_button = gr.Button("📝 Generate Lyrics from Tags")
            preset_lyrics_output = gr.Textbox(label="🎤 Lyrics Output", lines=12)

        with gr.TabItem("🧠 Guided Theme Mode"):
            guided_input = gr.Textbox(label="Describe Your Song Idea in 1 Sentence")
            guided_tags_output = gr.Textbox(label="Generated Tags", interactive=False)
            guided_generate_button = gr.Button("🧪 Generate Tags & Lyrics")
            guided_lyrics_output = gr.Textbox(label="🎤 Lyrics Output", lines=12)

    def generate_from_preset(style_name):
        tags = apply_preset_style(style_name)
        lyrics = generate_lyrics_from_tags(tags)
        return tags, lyrics

    def generate_from_description(desc):
        tags = guided_tag_wizard(desc)
        lyrics = generate_lyrics_from_tags(tags)
        return tags, lyrics

    apply_preset_button.click(generate_from_preset, inputs=preset_dropdown, outputs=[preset_tags_box, preset_lyrics_output])
    guided_generate_button.click(generate_from_description, inputs=guided_input, outputs=[guided_tags_output, guided_lyrics_output])

lyric_ui.launch()
