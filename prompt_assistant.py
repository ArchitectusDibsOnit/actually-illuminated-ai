# prompt_assistant.py

from metatag_model import generate_tags_from_text

PROMPT_TEMPLATES = {
    "song": "Write lyrics for a {genre} song with {mood} mood and theme of '{topic}'.",
    "script": "Draft a short script in the {genre} style, centered around '{topic}' and evoking a {mood} feeling.",
    "story": "Write a {genre} story about '{topic}', with an overall {mood} tone."
}

def suggest_prompt_from_idea(idea_text):
    tags = generate_tags_from_text(idea_text)
    genre = next((tag for tag in tags if tag in KNOWN_GENRES), "experimental")
    mood = next((tag for tag in tags if tag in MOOD_TAGS), "mysterious")
    topic = idea_text.strip()
    prompt_type = "song" if any(tag in idea_text.lower() for tag in ["sing", "lyrics", "music"]) else "story"
    
    template = PROMPT_TEMPLATES[prompt_type]
    return template.format(genre=genre, mood=mood, topic=topic)

# Example constants (can be loaded from meta config)
KNOWN_GENRES = ["hip hop", "synthwave", "folk", "metal", "pop", "orchestral", "jazz"]
MOOD_TAGS = ["happy", "sad", "angry", "dreamy", "epic", "mysterious"]
