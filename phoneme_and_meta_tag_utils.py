import re
import json
import os
import random
import gradio as gr

# Phoneme utilities for processing and generating phonetic representations
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

def load_phoneme_profiles():
    if os.path.exists(PHONEME_PROFILES_FILE):
        with open(PHONEME_PROFILES_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_phoneme_profile(profile_name, phoneme_data):
    profiles = load_phoneme_profiles()
    profiles[profile_name] = phoneme_data
    with open(PHONEME_PROFILES_FILE, 'w') as file:
        json.dump(profiles, file, indent=4)

def delete_phoneme_profile(profile_name):
    profiles = load_phoneme_profiles()
    if profile_name in profiles:
        del profiles[profile_name]
        with open(PHONEME_PROFILES_FILE, 'w') as file:
            json.dump(profiles, file, indent=4)
        return True
    return False

def apply_voice_morphing(phoneme_sequence, strength):
    phonemes = phoneme_sequence.split()
    morphed_phonemes = []
    for phoneme in phonemes:
        if random.random() < strength:
            random_phoneme = random.choice(list(set(phoneme_map.values()) - {phoneme}))
            morphed_phonemes.append(random_phoneme)
        else:
            morphed_phonemes.append(phoneme)
    return ' '.join(morphed_phonemes)

meta_tags = {
    "genres": ["[rock]", "[hip-hop]", "[jazz]", "[electronic]", "[metal]", "[classical]", "[pop]", "[ambient]", "[lo-fi]", "[dubstep]",
                "[blues]", "[country]", "[punk]", "[trap]", "[orchestral]", "[experimental]", "[multi-genre]", "[genre-flipping]"],
    "styles": ["[acoustic]", "[symphonic]", "[synthwave]", "[psychedelic]", "[minimalist]", "[melodic]", "[dissonant]", "[dark]", "[uplifting]"],
    "instruments": ["[guitar]", "[drums]", "[bass]", "[violin]", "[saxophone]", "[synthesizer]", "[piano]", "[trumpet]", "[flute]", "[orchestra]"],
    "notes": ["[A]", "[B]", "[C]", "[D]", "[E]", "[F]", "[G]"],
    "voices": ["[male]", "[female]", "[robotic]", "[alien]", "[deep]", "[high-pitched]", "[whispering]", "[screaming]", "[narrative-speaking]"],
    "themes": ["[comedic]", "[epic]", "[mysterious]", "[chaotic]", "[adventure]", "[satirical]", "[battle]", "[dreamlike]", "[retro]"],
    "sfx": ["[explosions]", "[vinyl crackles]", "[footsteps]", "[crowd noise]", "[ambient city sounds]", "[space sounds]", "[animal sounds]"]
}

def extract_meta_tags_from_prompt(prompt):
    return re.findall(r'\[(.*?)\]', prompt)

def get_tags(category):
    return meta_tags.get(category, [])

def validate_tags(prompt):
    all_tags = [tag for tags in meta_tags.values() for tag in tags]
    used_tags = [word for word in prompt.split() if word.startswith("[") and word.endswith("]")]
    invalid_tags = [tag for tag in used_tags if tag not in all_tags]
    return invalid_tags

def get_all_meta_tags():
    tag_summary = ""
    for category, tags in meta_tags.items():
        tag_summary += f"\n**{category.capitalize()}**: {', '.join(tags)}"
    return tag_summary

def phoneme_editor_interface():
    phoneme_profiles = load_phoneme_profiles()

    phoneme_name_input = gr.Textbox(label="Phoneme Profile Name")
    phoneme_string_input = gr.Textbox(label="Phoneme Sequence (space-separated phonemes)")
    save_button = gr.Button("💾 Save Phoneme Profile")

    phoneme_display = gr.Dropdown(choices=list(phoneme_profiles.keys()), label="Existing Profiles", multiselect=False)
    phoneme_output = gr.Textbox(label="Selected Profile Details", interactive=False)
    delete_button = gr.Button("🗑️ Delete Selected Profile")

    def save_phoneme(name, phoneme_string):
        if not name or not phoneme_string:
            return gr.update(choices=list(phoneme_profiles.keys())), "Name and phonemes required"
        phoneme_profiles[name] = phoneme_string
        save_phoneme_profile(name, phoneme_string)
        return gr.update(choices=list(phoneme_profiles.keys())), f"Saved: {name} -> {phoneme_string}"

    def show_phoneme(name):
        return phoneme_profiles.get(name, "Profile not found")

    def delete_phoneme(name):
        if name in phoneme_profiles:
            delete_phoneme_profile(name)
            phoneme_profiles.pop(name)
            return gr.update(choices=list(phoneme_profiles.keys())), "Profile deleted."
        return gr.update(), "Profile not found."

    save_button.click(save_phoneme, [phoneme_name_input, phoneme_string_input], [phoneme_display, phoneme_output])
    phoneme_display.change(show_phoneme, phoneme_display, phoneme_output)
    delete_button.click(delete_phoneme, phoneme_display, [phoneme_display, phoneme_output])

    return gr.Column([
        gr.Markdown("## 🔊 Phoneme Editor - Design and Save Custom Voices"),
        phoneme_name_input,
        phoneme_string_input,
        save_button,
        phoneme_display,
        phoneme_output,
        delete_button
    ])

def voice_morpher_interface():
    with gr.Blocks() as voice_morpher_ui:
        gr.Markdown("## 🎙️ Voice Morpher - Adjust and Transform Voice Profiles")

        input_phoneme = gr.Textbox(label="Input Phoneme Sequence")
        morph_strength = gr.Slider(0.0, 1.0, value=0.5, step=0.01, label="Morphing Strength")
        morph_button = gr.Button("⚡ Morph Voice")

        morphed_output = gr.Textbox(label="Morphed Phoneme Sequence", interactive=False)

        def morph_phoneme(input_seq, strength):
            return apply_voice_morphing(input_seq, strength)

        morph_button.click(morph_phoneme, [input_phoneme, morph_strength], morphed_output)

    return voice_morpher_ui
