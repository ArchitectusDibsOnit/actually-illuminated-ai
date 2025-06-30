import re
from phoneme_and_meta_tag_utils import load_phoneme_profiles

# Load voice profiles
voice_profiles = load_phoneme_profiles()


def parse_lyrics(lyrics_text):
    """
    Parses lyrics text and returns a structured sequence of segments with voice, meta-tags, and text.
    """
    pattern = re.compile(r"(\[.*?\])|(.*?)((?=\[)|$)")
    
    segments = []
    current_voice = None
    current_meta_tags = []

    for match in pattern.finditer(lyrics_text):
        tag = match.group(1)
        text = match.group(2).strip()

        if tag:
            if tag[1:-1] in voice_profiles:
                current_voice = tag[1:-1]
            else:
                current_meta_tags.append(tag)

        if text:
            segments.append({
                'voice': current_voice,
                'meta_tags': current_meta_tags.copy(),
                'text': text
            })
            current_meta_tags.clear()

    return segments


def display_parsed_lyrics(segments):
    """
    Display parsed segments in a readable format for debugging.
    """
    for i, segment in enumerate(segments):
        print(f"Segment {i + 1}:")
        print(f"  Voice: {segment['voice']}")
        print(f"  Meta-Tags: {' '.join(segment['meta_tags']) if segment['meta_tags'] else 'None'}")
        print(f"  Text: {segment['text']}\n")


if __name__ == "__main__":
    sample_lyrics = """
    [RockVoice] [screaming] This is [explosions] THE START! [HipHopVoice] [whispering] Quiet now... [symphonic] [alien] Echoes remain.
    """
    segments = parse_lyrics(sample_lyrics)
    display_parsed_lyrics(segments)
