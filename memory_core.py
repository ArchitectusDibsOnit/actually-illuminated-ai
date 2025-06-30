# memory_core.py

import gradio as gr
import json
import os

MEMORY_FILE = "memory_bank.json"

# Initialize memory structure
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as file:
            return json.load(file)
    else:
        return {"pronunciations": {}, "meta_tag_expansions": {}, "user_notes": {}}


def save_memory(memory):
    with open(MEMORY_FILE, 'w') as file:
        json.dump(memory, file, indent=4)


memory_bank = load_memory()


def add_pronunciation(word, phoneme_sequence):
    memory_bank["pronunciations"][word.lower()] = phoneme_sequence
    save_memory(memory_bank)
    return f"Saved pronunciation for '{word}' as '{phoneme_sequence}'"


def get_pronunciation(word):
    return memory_bank["pronunciations"].get(word.lower(), "Not found.")


def add_meta_tag_expansion(tag, description):
    memory_bank["meta_tag_expansions"][tag] = description
    save_memory(memory_bank)
    return f"Saved meta-tag expansion for '{tag}'."


def get_meta_tag_expansion(tag):
    return memory_bank["meta_tag_expansions"].get(tag, "Not found.")


def add_user_note(note):
    index = len(memory_bank["user_notes"]) + 1
    memory_bank["user_notes"][f"Note {index}"] = note
    save_memory(memory_bank)
    return f"Saved note {index}."


def clear_memory():
    global memory_bank
    memory_bank = {"pronunciations": {}, "meta_tag_expansions": {}, "user_notes": {}}
    save_memory(memory_bank)
    return "Memory cleared."


def memory_core_interface():
    with gr.Blocks() as memory_ui:
        gr.Markdown("## 🧠 Memory Core - Pronunciations, Meta-Tags, User Notes")

        with gr.Tab("Pronunciations"):
            word_input = gr.Textbox(label="Word")
            phoneme_input = gr.Textbox(label="Phoneme Sequence")
            save_pronunciation_button = gr.Button("Save Pronunciation")
            pronunciation_output = gr.Textbox(label="Memory Status", interactive=False)

            save_pronunciation_button.click(add_pronunciation, [word_input, phoneme_input], pronunciation_output)

        with gr.Tab("Meta-Tag Expansions"):
            tag_input = gr.Textbox(label="Meta-Tag (e.g. [explosions])")
            tag_description = gr.Textbox(label="Meta-Tag Description")
            save_tag_button = gr.Button("Save Meta-Tag Expansion")
            tag_output = gr.Textbox(label="Memory Status", interactive=False)

            save_tag_button.click(add_meta_tag_expansion, [tag_input, tag_description], tag_output)

        with gr.Tab("User Notes"):
            user_note_input = gr.Textbox(label="Enter Note")
            save_note_button = gr.Button("Save Note")
            note_output = gr.Textbox(label="Memory Status", interactive=False)

            save_note_button.click(add_user_note, user_note_input, note_output)

        with gr.Tab("Memory Management"):
            clear_button = gr.Button("Clear All Memory")
            clear_status = gr.Textbox(label="Memory Status", interactive=False)

            clear_button.click(clear_memory, None, clear_status)

    return memory_ui
