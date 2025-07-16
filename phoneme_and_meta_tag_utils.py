# phoneme_and_meta_tag_utils.py (Custom Meta-Tag Persistence + Phoneme Stub)

import re
import json
import os
import random

META_TAGS_FILE = "meta_tags.json"

# Load meta-tags from file or fallback defaults
if os.path.exists(META_TAGS_FILE):
    with open(META_TAGS_FILE, "r") as file:
        meta_tags = json.load(file)
else:
    meta_tags = {
        "genres": ["[rock]", "[hip-hop]", "[jazz]", "[electronic]", "[metal]", "[classical]", "[pop]", "[ambient]", "[lo-fi]", "[dubstep]"],
        "styles": ["[acoustic]", "[symphonic]", "[synthwave]", "[psychedelic]", "[minimalist]", "[melodic]", "[dissonant]", "[dark]", "[uplifting]"],
        "instruments": ["[guitar]", "[drums]", "[bass]", "[violin]", "[saxophone]", "[synthesizer]", "[piano]", "[trumpet]", "[flute]", "[orchestra]"],
        "voices": ["[male]", "[female]", "[robotic]", "[alien]", "[deep]", "[high-pitched]", "[whispering]", "[screaming]", "[narrative-speaking]"],
        "sfx": ["[explosions]", "[vinyl crackles]", "[footsteps]", "[crowd noise]", "[ambient city sounds]", "[space sounds]", "[animal sounds]"]
    }

def save_meta_tags():
    with open(META_TAGS_FILE, "w") as file:
        json.dump(meta_tags, file, indent=4)

def get_tags(category):
    return meta_tags.get(category, [])

def add_custom_tag(tag, category):
    if tag not in meta_tags[category]:
        meta_tags[category].append(tag)
        save_meta_tags()

def get_all_meta_tags():
    tag_summary = ""
    for category, tags in meta_tags.items():
        tag_summary += f"\n**{category.capitalize()}**: {', '.join(tags)}"
    return tag_summary

# ✅ Basic phoneme generator stub (replace with phonemizer later)
def text_to_phonemes(text):
    return " ".join([f"/{char}/" for char in text if char.isalnum()])
