# glyphclippy_ai.py

import gradio as gr

# Simple GlyphClippy memory
glyphclippy_memory = []

# GlyphClippy AI Logic
def glyphclippy_response(user_input):
    if "help" in user_input.lower():
        response = "📝 GlyphClippy says: 'Try selecting a module on the left to begin creating your sonic masterpiece! Need help with phonemes, timelines, or meta-tags? Just ask!'"
    elif "song" in user_input.lower():
        response = "🎶 GlyphClippy says: 'Use the Song Creation Wizard to build prompts with meta-tags and generate unique tracks!'"
    elif "performance" in user_input.lower():
        response = "⚙️ GlyphClippy says: 'Check the System Performance tab to benchmark your system and optimize frame-slicing!'"
    elif "timeline" in user_input.lower():
        response = "🕰️ GlyphClippy says: 'Manage voice and phoneme timelines using the Voice Timeline and Phoneme Onset/Offset Editor!'"
    elif "who are you" in user_input.lower():
        response = "✨ GlyphClippy says: 'I’m GlyphClippy, your memetic sonic creation assistant. Let’s make some chaos!'"
    else:
        response = "🤔 GlyphClippy says: 'I didn’t catch that. Try asking about songs, phonemes, timelines, or system performance!'"

    glyphclippy_memory.append({"user": user_input, "glyphclippy": response})
    return response

# GlyphClippy Interface
def glyphclippy_interface():
    with gr.Blocks() as clippy_ui:
        gr.Markdown("## 🤖 GlyphClippy - Your Sonic Creation Assistant")

        with gr.Row():
            user_input = gr.Textbox(label="Ask GlyphClippy Something", lines=1)
            clippy_response = gr.Textbox(label="GlyphClippy's Response", interactive=False)

        ask_button = gr.Button("Ask GlyphClippy")

        ask_button.click(fn=glyphclippy_response, inputs=user_input, outputs=clippy_response)

    return clippy_ui
