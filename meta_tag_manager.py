# meta_tag_manager.py

import json
import difflib
import os

META_TAG_FILE = "meta_tags.json"

def load_meta_tags():
    """Load meta-tags from JSON file."""
    if os.path.exists(META_TAG_FILE):
        with open(META_TAG_FILE, "r") as f:
            return json.load(f)
    else:
        return []

def save_meta_tags(tags):
    """Save meta-tags to JSON file."""
    with open(META_TAG_FILE, "w") as f:
        json.dump(tags, f, indent=4)

def validate_meta_tags(tags, known_tags):
    """Split valid and invalid tags."""
    valid = [tag for tag in tags if tag in known_tags]
    invalid = [tag for tag in tags if tag not in known_tags]
    return valid, invalid

def suggest_similar_tags(tag, known_tags, cutoff=0.6):
    """Suggest similar known tags for a given invalid tag."""
    return difflib.get_close_matches(tag, known_tags, n=5, cutoff=cutoff)

def enrich_tags(tags, known_tags):
    """Automatically expand tags using related associations (basic heuristic for now)."""
    expanded = set(tags)
    for tag in tags:
        if tag == "[metal]":
            expanded.update(["[distorted]", "[scream]", "[heavy]", "[guitar solo]"])
        elif tag == "[lofi]":
            expanded.update(["[study]", "[instrumental]", "[chill]", "[tape hiss]"])
        elif tag == "[robotic]":
            expanded.update(["[vocoder]", "[glitch]", "[electronic]"])
        elif tag == "[anime]":
            expanded.update(["[jpop]", "[energetic]", "[cute]"])
    return list(expanded)

if __name__ == "__main__":
    print("Meta-tag manager ready.")
