# lyrics_ui.py

import gradio as gr
from lyrics_parser import parse_lyrics

def lyrics_interface():
    with gr.Blocks() as lyrics_ui:
        gr.Markdown("## 🎶 Lyrics Input and Meta-Tag Parser")

        with gr.Row():
            lyrics_input = gr.Textbox(label="Enter Song Lyrics with Meta-Tags", lines=10)

        with gr.Row():
            parse_button = gr.Button("Parse Lyrics")
            clear_button = gr.Button("Clear")

        parsed_output = gr.Textbox(label="Parsed Lyrics", lines=10, interactive=False)

        parse_button.click(lambda lyrics: parse_lyrics(lyrics), lyrics_input, parsed_output)
        clear_button.click(lambda: "", None, parsed_output)

    return lyrics_ui
