# Actually Illuminated AI - File Review and Integration Canvas

# 📦 System Cleanup and File Consolidation (Final Structure)

---

# 🎛️ audio_utils.py (Merged Utilities)

import numpy as np
import soundfile as sf
import librosa
import torchaudio
import torch
import os


def save_audio(filename, audio_array, sampling_rate):
    sf.write(filename, audio_array, sampling_rate)



def load_audio(filename, target_sr=16000):
    if filename.endswith('.wav'):
        audio, sr = librosa.load(filename, sr=target_sr)
        return audio, sr
    else:
        waveform, sample_rate = torchaudio.load(filename)
        return waveform, sample_rate



def normalize_audio(audio_array):
    return audio_array / np.max(np.abs(audio_array))



def pitch_shift(audio_array, sr, n_steps):
    return librosa.effects.pitch_shift(audio_array, sr, n_steps)



def time_stretch(audio_array, rate):
    return librosa.effects.time_stretch(audio_array, rate)



def apply_reverb(audio_array, sr, reverberance=50):
    impulse_response = np.zeros(int(sr * 0.1))
    impulse_response[0] = 1.0
    impulse_response[int(sr * 0.05)] = reverberance / 100.0
    reverbed = np.convolve(audio_array, impulse_response, mode='full')
    return reverbed[:len(audio_array)]



def convert_to_wav(input_path, output_path):
    waveform, sample_rate = load_audio(input_path)
    save_audio(output_path, waveform.numpy().squeeze(), sample_rate)



# 🎙️ phoneme_and_meta_tag_utils.py (Merged and Expanded)

import re
import json
import os
import random

phoneme_map = {
    'A': 'æ', 'B': 'b', 'C': 'k', 'D': 'd', 'E': 'ɛ', 'F': 'f', 'G': 'ɡ',
    'H': 'h', 'I': 'ɪ', 'J': 'dʒ', 'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n',
    'O': 'ɔ', 'P': 'p', 'Q': 'kw', 'R': 'ɹ', 'S': 's', 'T': 't', 'U': 'ʊ',
    'V': 'v', 'W': 'w', 'X': 'ks', 'Y': 'j', 'Z': 'z'
}

PHONEME_PROFILES_FILE = "phoneme_profiles.json"

meta_tags = {
    "styles": ["[rock]", "[hip-hop]", "[jazz]", "[electronic]", "[metal]", "[classical]", "[pop]", "[ambient]", "[lo-fi]", "[dubstep]",
                "[blues]", "[country]", "[punk]", "[trap]", "[orchestral]", "[experimental]", "[multi-genre]", "[genre-flipping]"],
    "voices": ["[male]", "[female]", "[robotic]", "[alien]", "[deep]", "[high-pitched]", "[whispering]", "[screaming]", "[narrative-speaking]"],
    "music_sfx_glyphs": ["[guitar]", "[drums]", "[bass]", "[violin]", "[saxophone]", "[synthesizer]", "[piano]", "[trumpet]", "[flute]", "[orchestra]",
                        "[A]", "[B]", "[C]", "[D]", "[E]", "[F]", "[G]",
                        "[comedic]", "[epic]", "[mysterious]", "[chaotic]", "[adventure]", "[satirical]", "[battle]", "[dreamlike]", "[retro]",
                        "[explosions]", "[vinyl crackles]", "[footsteps]", "[crowd noise]", "[ambient city sounds]", "[space sounds]", "[animal sounds]"]
}


# 🎚️ Audio & Phoneme Utilities

# Text to phonemes
def text_to_phonemes(text):
    phonemes = []
    for char in text.upper():
        if char in phoneme_map:
            phonemes.append(phoneme_map[char])
        else:
            phonemes.append(char)
    return ' '.join(phonemes)


# Phoneme sequence to text
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


# Validate phoneme sequence
def validate_phoneme_sequence(phoneme_sequence):
    pattern = re.compile(r"^[æbkdɛfɡhɪdʒklmnɔpkwɹstʊvwxjz\s]+$")
    return bool(pattern.match(phoneme_sequence))


# Phoneme Profile Management
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


# Voice Morphing
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


# Meta-Tag Utilities
def get_tags(category):
    return meta_tags.get(category, [])



def validate_tags(prompt):
    all_tags = [tag for tags in meta_tags.values() for tag in tags]
    used_tags = [word for word in prompt.split() if word.startswith("[") and word.endswith("]")]
    invalid_tags = [tag for tag in used_tags if tag not in all_tags]
    return invalid_tags



def get_all_meta_tags():
    tag_summary = ""
    tag_summary += f"\n**Style/Genre (meta-tags)**: {', '.join(meta_tags['styles'])}"
    tag_summary += f"\n**Vocal/Character Description (meta-tags)**: {', '.join(meta_tags['voices'])}"
    tag_summary += f"\n**Music/SFX/Glyph Tags (meta-tags)**: {', '.join(meta_tags['music_sfx_glyphs'])}"
    return tag_summary


# ✅ First Upgrade Package Ready ✅

# ✅ Second Package Ready ✅
# Launcher Integration Finalization
# Glyphscribe Integration
# UI Expansion
# Deprecated File Cleanup
# Lyrics Parsing Engine Integration


# ✅ Third Package In Progress ✅
# Lyrics UI Tab + Live Parsing Display
# Real-Time Preview Engine
# Playback Emulator for Meta-Tags


# 🎤 lyrics_ui.py (Integrated UI)

import gradio as gr
from lyrics_parser import parse_lyrics



def lyrics_interface():
    with gr.Blocks() as lyrics_ui:
        gr.Markdown("## 🎶 Lyrics Input and Meta-Tag Parser")

        with gr.Row():
            lyrics_input = gr.Textbox(label="Enter Song Lyrics with Meta-Tags", lines=10)

        with gr.Row():
            parse_button = gr.Button("Parse Lyrics")
            clear_button = gr.Button("Clear")

        parsed_output = gr.Textbox(label="Parsed Lyrics", lines=10, interactive=False)

        parse_button.click(lambda lyrics: parse_lyrics(lyrics), lyrics_input, parsed_output)
        clear_button.click(lambda: "", None, parsed_output)

    return lyrics_ui


# 🎧 playback_emulator.py (Integrated Playback Emulator)

import gradio as gr



def playback_emulator_interface():
    with gr.Blocks() as playback_emulator:
        gr.Markdown("## 🔉 Meta-Tag Playback Emulator (Coming Soon)")
        gr.Markdown("This will allow real-time meta-tag sound testing and preview.")

    return playback_emulator


# 🎛️ voice_timeline_editor.py (Integrated Voice Timeline Editor)

import gradio as gr


voice_timeline = []


def add_voice_entry(start_time, end_time, description):
    entry = {"start": start_time, "end": end_time, "description": description}
    voice_timeline.append(entry)
    return render_timeline()


def clear_voice_timeline():
    global voice_timeline
    voice_timeline = []
    return render_timeline()


def render_timeline():
    if not voice_timeline:
        return "No voice entries defined."
    timeline_display = "\n".join([f"{entry['start']}s - {entry['end']}s: {entry['description']}" for entry in voice_timeline])
    return timeline_display


def voice_timeline_editor_interface():
    with gr.Blocks() as timeline_ui:
        gr.Markdown("## 🎼 Voice Timeline Editor")

        with gr.Row():
            start_input = gr.Number(label="Start Time (seconds)")
            end_input = gr.Number(label="End Time (seconds)")
            description_input = gr.Textbox(label="Voice Description")

        add_button = gr.Button("Add Voice Segment")
        clear_button = gr.Button("Clear Timeline")

        timeline_output = gr.Textbox(label="Voice Timeline", lines=10, interactive=False)

        add_button.click(add_voice_entry, [start_input, end_input, description_input], timeline_output)
        clear_button.click(clear_voice_timeline, None, timeline_output)

    return timeline_ui
