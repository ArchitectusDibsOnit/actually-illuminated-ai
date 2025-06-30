# 🔥 Memory Bank System - Actually Illuminated AI 🔥

import json
import os

MEMORY_BANK_FILE = "phonemic_memory_bank.json"

# Initialize memory bank if it doesn't exist
def load_memory_bank():
    if os.path.exists(MEMORY_BANK_FILE):
        with open(MEMORY_BANK_FILE, 'r') as file:
            return json.load(file)
    else:
        return {"words": {}, "pronunciations": {}, "meta_tag_sounds": {}}


def save_memory_bank(memory_bank):
    with open(MEMORY_BANK_FILE, 'w') as file:
        json.dump(memory_bank, file, indent=4)


# Core memory bank management
memory_bank = load_memory_bank()


# Add word with phonemes and optional sound samples
def add_word_to_memory(word, phoneme_sequence, pronunciation_variants=None):
    memory_bank['words'][word.lower()] = {
        "phonemes": phoneme_sequence,
        "pronunciations": pronunciation_variants or []
    }
    save_memory_bank(memory_bank)


# Retrieve word data
def get_word_from_memory(word):
    return memory_bank['words'].get(word.lower(), None)


# Add pronunciation variant with audio examples
def add_pronunciation_variant(word, phoneme_sequence, audio_path=None):
    if word.lower() not in memory_bank['words']:
        add_word_to_memory(word, phoneme_sequence)

    memory_bank['words'][word.lower()]['pronunciations'].append({
        "phonemes": phoneme_sequence,
        "audio": audio_path
    })
    save_memory_bank(memory_bank)


# Save meta-tag sounds
def add_meta_tag_sound(meta_tag, audio_path):
    memory_bank['meta_tag_sounds'][meta_tag] = audio_path
    save_memory_bank(memory_bank)


# Retrieve pronunciation options
def list_pronunciations(word):
    word_data = get_word_from_memory(word)
    if word_data:
        return word_data.get('pronunciations', [])
    return []


# Retrieve meta-tag sound
def get_meta_tag_sound(meta_tag):
    return memory_bank['meta_tag_sounds'].get(meta_tag, None)


# Memory editing tools
def delete_word_from_memory(word):
    if word.lower() in memory_bank['words']:
        del memory_bank['words'][word.lower()]
        save_memory_bank(memory_bank)


# Ensure no square-bracket meta-tags are processed as words
def is_meta_tag(word):
    return word.startswith('[') and word.endswith(']')


# Build ETA integration
def estimate_processing_time(lyrics, phoneme_speed=0.05):
    word_count = len([word for word in lyrics.split() if not is_meta_tag(word)])
    estimated_time = word_count * phoneme_speed
    return round(estimated_time, 2)


print("[✔] Memory Bank System Ready.")
