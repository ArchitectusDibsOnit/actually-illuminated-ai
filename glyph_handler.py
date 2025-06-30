import json
import os

GLYPH_DATABASE_FILE = "glyph_database.json"

def load_glyph_database():
    if os.path.exists(GLYPH_DATABASE_FILE):
        with open(GLYPH_DATABASE_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_glyph_database(glyphs):
    with open(GLYPH_DATABASE_FILE, 'w') as file:
        json.dump(glyphs, file, indent=4)

def add_glyph(glyph_name, glyph_data):
    glyphs = load_glyph_database()
    glyphs[glyph_name] = glyph_data
    save_glyph_database(glyphs)

def get_glyph(glyph_name):
    glyphs = load_glyph_database()
    return glyphs.get(glyph_name, None)

def list_glyphs():
    glyphs = load_glyph_database()
    return list(glyphs.keys())

def delete_glyph(glyph_name):
    glyphs = load_glyph_database()
    if glyph_name in glyphs:
        del glyphs[glyph_name]
        save_glyph_database(glyphs)
        return True
    return False

def load_glyphs():
    return load_glyph_database()

def save_glyphs(glyphs):
    save_glyph_database(glyphs)

def display_glyphs():
    glyphs = load_glyph_database()
    if not glyphs:
        return "No glyphs found."
    return "\n".join([f"{name}: {data}" for name, data in glyphs.items()])

