# subtitle_exporter.py

import os

def export_subtitles(lyrics, timeline_log, song_name, format="srt"):
    output_dir = "subtitles"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{song_name}.{format}")

    lines = []
    for idx, entry in enumerate(timeline_log, start=1):
        start = entry["start_time"]
        end = entry["end_time"]
        voice = entry["voice"]
        text = entry["lyrics"]

        start_str = format_time(start)
        end_str = format_time(end)

        lines.append(f"{idx}\n{start_str} --> {end_str}\n[{voice}]: {text}\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[✔] Subtitles exported to: {file_path}")
    return file_path

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
