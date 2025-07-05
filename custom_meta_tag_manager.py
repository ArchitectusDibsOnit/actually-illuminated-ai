# custom_meta_tag_manager.py

import json
import os

CUSTOM_TAGS_FILE = "custom_meta_tags.json"

def load_custom_tags():
    if os.path.exists(CUSTOM_TAGS_FILE):
        with open(CUSTOM_TAGS_FILE, "r") as file:
            return json.load(file)
    return {"genres": [], "styles": [], "voices": [], "instruments": [], "sfx": []}

def save_custom_tags(tags):
    with open(CUSTOM_TAGS_FILE, "w") as file:
        json.dump(tags, file, indent=4)

def add_custom_tag(category, new_tag):
    tags = load_custom_tags()
    if category not in tags:
        tags[category] = []
    if new_tag not in tags[category]:
        tags[category].append(new_tag)
    save_custom_tags(tags)

def get_combined_tags(base_tags, category):
    custom_tags = load_custom_tags().get(category, [])
    return base_tags + custom_tags
