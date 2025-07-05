import re
import json
import os
import random
import gradio as gr

# Meta-tag storage file
META_TAGS_FILE = "meta_tags.json"

# Default meta-tag structure
default_meta_tags = {
    "genres": ["[rock]", "[hip-hop]", "[jazz]", "[electronic]", "[metal]", "[classical]", "[pop]", "[ambient]", "[lo-fi]", "[dubstep]"],
    "styles": ["[acoustic]", "[symphonic]", "[synthwave]", "[psychedelic]", "[minimalist]", "[melodic]", "[dissonant]", "[dark]", "[uplifting]"],
    "voices": ["[male]", "[female]", "[robotic]", "[alien]", "[deep]", "[high-pitched]", "[whispering]", "[screaming]", "[narrative-speaking]"],
    "instruments": ["[guitar]", "[drums]", "[bass]", "[violin]", "[saxophone]", "[synthesizer]", "[piano]", "[trumpet]", "[flute]", "[orchestra]"],
    "sfx": ["[explosions]", "[vinyl crackles]", "[footsteps]", "[crowd noise]", "[ambient city sounds]", "[space sounds]", "[animal sounds]"]
}

# Load or initialize meta-tags
if os.path.exists(META_TAGS_FILE):
    with open(META_TAGS_FILE, 'r') as file:
        meta_tags = json.load(file)
else:
    meta_tags = default_meta_tags
    with open(META_TAGS_FILE, 'w') as file:
        json.dump(meta_tags, file, indent=4)

# --------- Meta-Tag Utilities ---------
def save_meta_tags():
    with open(META_TAGS_FILE, 'w') as file:
        json.dump(meta_tags, file, indent=4)

def get_tags(category):
    return meta_tags.get(category, [])

def get_all_meta_tags():
    tag_summary = ""
    for category, tags in meta_tags.items():
        tag_summary += f"\n**{category.capitalize()}**: {', '.join(tags)}"
    return tag_summary

def validate_tags(prompt):
    all_tags = [tag for tags in meta_tags.values() for tag in tags]
    used_tags = [word for word in prompt.split() if word.startswith("[") and word.endswith("]")]
    invalid_tags = [tag for tag in used_tags if tag not in all_tags]
    return invalid_tags

def add_custom_tag(category, new_tag):
    if new_tag not in meta_tags[category]:
        meta_tags[category].append(new_tag)
        save_meta_tags()

# --------- Existing Phoneme Utilities ---------
phoneme_map = {
    'A': 'æ', 'B': 'b', 'C': 'k', 'D': 'd', 'E': 'ɛ', 'F': 'f', 'G': 'ɡ',
    'H': 'h', 'I': 'ɪ', 'J': 'dʒ', 'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n',
    'O': 'ɔ', 'P': 'p', 'Q': 'kw', 'R': 'ɹ', 'S': 's', 'T': 't', 'U': 'ʊ',
    'V': 'v', 'W': 'w', 'X': 'ks', 'Y': 'j', 'Z': 'z'
}

PHONEME_PROFILES_FILE = "phoneme_profiles.json"

def text_to_phonemes(text):
    phonemes = []
    for char in text.upper():
        if char in phoneme_map:
            phonemes.append(phoneme_map[char])
        else:
            phonemes.append(char)
    return ' '.join(phonemes)

def phoneme_sequence_to_text(phoneme_sequence):
    reverse_map = {v: k for k, v in phoneme_map.items()}
    words = phoneme_sequence.split()
    text = ''
    for phoneme in words:
        if phoneme in reverse_map:
            text += reverse_map[phoneme]
        else:
            text += phoneme
    return text

def validate_phoneme_sequence(phoneme_sequence):
    pattern = re.compile(r"^[æbkdɛfɡhɪdʒklmnɔpkwɹstʊvwxjz\s]+$")
    return bool(pattern.match(phoneme_sequence))
