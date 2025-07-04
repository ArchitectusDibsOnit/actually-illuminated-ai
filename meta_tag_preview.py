# meta_tag_preview.py

import os
import gradio as gr
from audio_utils import load_audio, normalize_audio
import sounddevice as sd

META_TAG_SAMPLES_FOLDER = "assets/meta_tag_samples"

# Load available samples for meta-tags
def load_meta_tag_samples():
    samples = {}
    if not os.path.exists(META_TAG_SAMPLES_FOLDER):
        os.makedirs(META_TAG_SAMPLES_FOLDER)

    for file in os.listdir(META_TAG_SAMPLES_FOLDER):
        if file.endswith(".wav") or file.endswith(".mp3") or file.endswith(".ogg"):
            tag = f"[{os.path.splitext(file)[0]}]"
            samples[tag.lower()] = os.path.join(META_TAG_SAMPLES_FOLDER, file)

    return samples


# Preview sound by meta-tag
def preview_meta_tag_sound(tag):
    tag = tag.lower()
    if tag in meta_tag_samples:
        audio_path = meta_tag_samples[tag]
        audio_array, sr = load_audio(audio_path)
        audio_array = normalize_audio(audio_array)
        sd.play(audio_array, sr)
        return f"🔊 Playing: {tag}"
    else:
        return f"⚠️ No sample found for {tag}"


# Initialize on load
meta_tag_samples = load_meta_tag_samples()


# Build UI
def meta_tag_preview_ui():
    with gr.Blocks() as preview_ui:
        gr.Markdown("## 🎧 Meta-Tag Sound Preview")

        available_tags = list(meta_tag_samples.keys())

        tag_selector = gr.Dropdown(choices=available_tags, label="Select Meta-Tag to Preview")
        play_button = gr.Button("▶️ Play Sample")
        status_output = gr.Textbox(label="Status", interactive=False)

        play_button.click(preview_meta_tag_sound, tag_selector, status_output)

    return preview_ui

#meta_tag_autocomplete.py:
# meta_tag_autocomplete.py

from phoneme_and_meta_tag_utils import meta_tags

def get_all_tags_flat():
    tags = []
    for category in meta_tags.values():
        tags.extend(category)
    return tags

def filter_tags(user_input):
    if not user_input.startswith("["):
        return []
    return [tag for tag in get_all_tags_flat() if tag.startswith(user_input)]


