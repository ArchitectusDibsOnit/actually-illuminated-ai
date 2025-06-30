# user_meta_tag_builder.py

import gradio as gr
import json
import os

USER_TAGS_FILE = "user_meta_tags.json"

def load_user_tags():
    if os.path.exists(USER_TAGS_FILE):
        with open(USER_TAGS_FILE, 'r') as file:
            return json.load(file)
    else:
        return {"styles": [], "voices": [], "sfx": []}


def save_user_tags(tags):
    with open(USER_TAGS_FILE, 'w') as file:
        json.dump(tags, file, indent=4)


user_tags = load_user_tags()


def add_user_meta_tag(tag, category):
    tag = tag.strip()
    if category not in user_tags:
        return f"Invalid category: {category}"
    if tag in user_tags[category]:
        return f"Tag '{tag}' already exists in {category}."

    user_tags[category].append(tag)
    save_user_tags(user_tags)
    return f"Added '{tag}' to {category}."


def display_user_tags():
    display = ""
    for category, tags in user_tags.items():
        display += f"**{category.capitalize()} Tags:** {', '.join(tags) if tags else 'None'}\n"
    return display


def clear_user_tags():
    global user_tags
    user_tags = {"styles": [], "voices": [], "sfx": []}
    save_user_tags(user_tags)
    return "User-defined tags cleared."


def user_meta_tag_builder_interface():
    with gr.Blocks() as tag_ui:
        gr.Markdown("## 🏷️ User Meta-Tag Builder")

        with gr.Row():
            tag_input = gr.Textbox(label="Meta-Tag (Example: [new_sound])")
            category_input = gr.Dropdown(choices=["styles", "voices", "sfx"], label="Select Category")

        add_button = gr.Button("Add Meta-Tag")
        clear_button = gr.Button("Clear All User Tags")

        tag_status = gr.Textbox(label="Status", interactive=False)
        tag_display = gr.Markdown(display_user_tags())

        def refresh_tags():
            return display_user_tags()

        add_button.click(add_user_meta_tag, [tag_input, category_input], tag_status).then(
            lambda: refresh_tags(), None, tag_display
        )

        clear_button.click(clear_user_tags, None, tag_status).then(
            lambda: refresh_tags(), None, tag_display
        )

    return tag_ui
