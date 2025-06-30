# song_structure_parser.py

def parse_song_structure(song_prompt):
    import re
    structure = []
    sections = re.findall(r'\[(.*?)\](.*?)(?=\[|$)', song_prompt, re.DOTALL)

    timestamp = 0  # Initialize timestamp in seconds (could evolve later)
    section_duration = 10  # Default section length in seconds (adjustable later)

    for tag, content in sections:
        structure.append({
            "section": tag.strip(),
            "lyrics": content.strip(),
            "start_time": timestamp,
            "end_time": timestamp + section_duration
        })
        timestamp += section_duration  # Increment timestamp

    return structure
