# 🎛️ meta_tag_builder.py

import gradio as gr
import json
import os

META_TAGS_FILE = "user_meta_tags.json"

# Load and Save Meta-Tags

def load_user_meta_tags():
    if os.path.exists(META_TAGS_FILE):
        with open(META_TAGS_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}


def save_user_meta_tags(tags):
    with open(META_TAGS_FILE, 'w') as file:
        json.dump(tags, file, indent=4)


# Meta-Tag Builder UI

def meta_tag_builder_interface():
    user_tags = load_user_meta_tags()

    tag_name_input = gr.Textbox(label="Meta-Tag Name (use brackets like [MyTag])")
    tag_category_input = gr.Dropdown(choices=["styles", "voices", "music_sfx_glyphs", "tone", "accent"], label="Meta-Tag Category")
    tag_description_input = gr.Textbox(label="Meta-Tag Description")
    tag_sound_file_input = gr.File(label="Upload Associated Sound File (optional)")
    save_button = gr.Button("💾 Save Meta-Tag")

    status_output = gr.Textbox(label="Status", interactive=False)

    def save_meta_tag(tag_name, category, description, sound_file):
        if not tag_name or not category:
            return "⚠️ Tag Name and Category are required."

        if tag_name[0] != '[' or tag_name[-1] != ']':
            return "⚠️ Tag Name must be in square brackets like [MyTag]."

        user_tags[tag_name] = {
            "category": category,
            "description": description,
            "sound_file": sound_file.name if sound_file else None
        }

        save_user_meta_tags(user_tags)
        return f"✅ Saved {tag_name} to {category}"

    save_button.click(
        save_meta_tag,
        inputs=[tag_name_input, tag_category_input, tag_description_input, tag_sound_file_input],
        outputs=status_output
    )

    return gr.Column([
        gr.Markdown("## 🏗️ Meta-Tag Builder - Create Custom Meta-Tags"),
        tag_name_input,
        tag_category_input,
        tag_description_input,
        tag_sound_file_input,
        save_button,
        status_output
    ])
