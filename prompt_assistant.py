# prompt_assistant.py (Expanded with Preset Styles + Guided Description Mode + Tag Expansion)

import gradio as gr
from meta_tag_manager import detect_tags, get_all_known_tags

# Example preset style tag combos
PRESET_STYLES = {
    "Epic Cinematic": ["[cinematic]", "[epic]", "[orchestral]"],
    "Dark Trap": ["[trap]", "[dark]", "[808-heavy]"],
    "Hyperpop Chaos": ["[hyperpop]", "[distorted]", "[maximalist]"],
    "Lo-fi Chill": ["[lofi]", "[chill]", "[ambient]"],
    "Anime Opening": ["[anime]", "[upbeat]", "[jpop]"],
}

def suggest_prompt_from_idea(idea):
    tags = detect_tags(idea)
    return " ".join(tags)

def get_preset_styles():
    return list(PRESET_STYLES.keys())

def apply_preset_style(style_name):
    return " ".join(PRESET_STYLES.get(style_name, []))

def guided_tag_wizard(description):
    tags = detect_tags(description)
    lower_desc = description.lower()
    if "sad" in lower_desc:
        tags.append("[sad]")
    if "fast" in lower_desc or "upbeat" in lower_desc:
        tags.append("[fast-tempo]")
    if "dark" in lower_desc:
        tags.append("[dark]")
    if "emotional" in lower_desc:
        tags.append("[emotional]")
    return " ".join(sorted(set(tags)))

def tag_browser():
    return " ".join(sorted(get_all_known_tags()))

with gr.Blocks() as prompt_ui:
    gr.Markdown("## ✨ Prompt Assistant with Presets, Guided Tags, and Tag Browser")

    with gr.Row():
        style_dropdown = gr.Dropdown(label="🎨 Preset Style", choices=get_preset_styles())
        style_tags_output = gr.Textbox(label="🎯 Tags from Preset", interactive=False)
        style_button = gr.Button("🎬 Apply Style")

    with gr.Row():
        guided_input = gr.Textbox(label="🧠 Describe Your Idea (1 sentence)")
        guided_tags_output = gr.Textbox(label="🔖 Generated Tags", interactive=False)
        guided_button = gr.Button("🧪 Generate Tags from Description")

    with gr.Row():
        all_tags_display = gr.Textbox(label="📚 All Known Meta-Tags", interactive=False, lines=5)
        tag_browser_button = gr.Button("🔍 Show All Tags")

    style_button.click(apply_preset_style, inputs=style_dropdown, outputs=style_tags_output)
    guided_button.click(guided_tag_wizard, inputs=guided_input, outputs=guided_tags_output)
    tag_browser_button.click(tag_browser, outputs=all_tags_display)
