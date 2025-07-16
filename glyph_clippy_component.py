# glyph_clippy_component.py
import gradio as gr

def GlyphClippy():
    with gr.Box(elem_id="glyph-clippy-box"):
        with gr.Row():
            gr.Image(
                value="glyphclippy_idle.png",  # Path to your floating avatar image
                label="GlyphClippy",
                show_label=False,
                interactive=False
            )
        gr.Markdown("**Need help?** Click here or ask away!", elem_id="glyph-clippy-text")
    return gr.update(visible=True)
