# nlp_memory_parser.py

import json
import os

MEMORY_FILE = "nlp_memory.json"

def load_nlp_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_nlp_memory(memory):
    with open(MEMORY_FILE, 'w') as file:
        json.dump(memory, file, indent=4)

def remember_word_pronunciation(word, pronunciation):
    memory = load_nlp_memory()
    memory[word] = pronunciation
    save_nlp_memory(memory)

def get_word_pronunciation(word):
    memory = load_nlp_memory()
    return memory.get(word, None)

def suggest_pronunciation(word):
    return get_word_pronunciation(word) or "Default phoneme sequence"
