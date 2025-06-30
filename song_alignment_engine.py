# song_alignment_engine.py

from song_structure_parser import parse_song_structure

def align_song_with_voices(song_prompt, voice_timeline):
    song_structure = parse_song_structure(song_prompt)
    alignment_log = []

    for section in song_structure:
        matching_voices = [
            entry for entry in voice_timeline
            if section["start_time"] <= entry["start_time"] <= section["end_time"]
        ]

        alignment_log.append({
            "section": section["section"],
            "lyrics": section["lyrics"],
            "voices": matching_voices if matching_voices else [{"voice": "Default Voice", "lyrics": section["lyrics"]}]
        })

    return alignment_log
