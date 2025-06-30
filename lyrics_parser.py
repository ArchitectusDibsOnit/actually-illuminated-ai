import re

# Splits lyrics into sections with meta-tags and optional voice switches
def parse_lyrics(lyrics_text):
    pattern = r"(\[[^\]]+\])"
    tokens = re.split(pattern, lyrics_text)

    parsed = []
    current_tags = []
    current_voice = None

    for token in tokens:
        if not token.strip():
            continue
        if token.startswith("[") and token.endswith("]"):
            tag = token[1:-1].strip()
            if tag.lower() in ['male', 'female', 'robotic', 'alien', 'voice1', 'voice2', 'voice3']:
                current_voice = tag
            else:
                current_tags.append(tag)
        else:
            parsed.append({
                'text': token.strip(),
                'voice': current_voice,
                'meta_tags': current_tags.copy()
            })
            current_tags = []

    return parsed
