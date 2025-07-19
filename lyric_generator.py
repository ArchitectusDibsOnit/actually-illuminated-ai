# lyric_generator.py
# Generates lyrics from a short prompt/theme using Suno-style formatting and meta-tags

import random
from meta_tag_manager import detect_tags

# Constants
MAX_LYRIC_LENGTH = 3000
CHORUS_PROB = 0.2
VERSE_COUNT = 2
CHORUS_REPEAT = 2

# Lyric templates
VERSE_TEMPLATES = [
    "{theme}, now it's time to feel the {vibe}\nWe ride the beat like waves and never hide\n{image}, stuck inside my mind\nHoping that the {light} helps us realign\n",
    "In the {setting} where the {thing} cry\n{theme} burning in the sky\n{verb} my name into the night\nLet the {emotion} guide me right\n"
]

CHORUS_TEMPLATES = [
    "This is our {anthem}, {echo}, never stop\n{theme} rising till we reach the top\nWe got that {energy}, let it drop\n{hook}, we can’t be stopped\n",
    "{hook} like the sound of fate\n{theme} always resonates\n{echo}, no escape\nOur {anthem} won't deflate\n"
]

FILLER_WORDS = {
    "vibe": ["energy", "madness", "vibration"],
    "image": ["mirror", "vision", "silhouette"],
    "light": ["sun", "flame", "glow"],
    "setting": ["shadows", "neon halls", "storm"],
    "thing": ["angels", "sirens", "ghosts"],
    "verb": ["scream", "carve", "burn"],
    "emotion": ["pain", "fire", "passion"],
    "anthem": ["anthem", "chorus", "pulse"],
    "echo": ["echo", "rumble", "cry"],
    "energy": ["hype", "storm", "roar"],
    "hook": ["hook", "chant", "rally cry"]
}

def fill_template(template, theme):
    output = template
    for key in FILLER_WORDS:
        output = output.replace("{" + key + "}", random.choice(FILLER_WORDS[key]))
    output = output.replace("{theme}", theme)
    return output

def generate_lyrics(theme, tags=[], include_chorus=True):
    lyrics = ""
    tags_str = " ".join(tags) if tags else " ".join(detect_tags(theme))
    lyrics += tags_str + "\n\n"

    for _ in range(VERSE_COUNT):
        verse = fill_template(random.choice(VERSE_TEMPLATES), theme)
        lyrics += verse + "\n"
        if include_chorus and random.random() < CHORUS_PROB:
            chorus = fill_template(random.choice(CHORUS_TEMPLATES), theme)
            lyrics += chorus * CHORUS_REPEAT + "\n"

    return lyrics.strip()[:MAX_LYRIC_LENGTH]

if __name__ == "__main__":
    test_theme = "dreams of digital rebellion"
    print(generate_lyrics(test_theme))
