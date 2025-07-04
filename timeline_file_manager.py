# timeline_file_manager.py

import json
import os

from song_structure_manager import timeline as song_timeline
from voice_timeline_sync_engine import voice_timeline

SAVE_FOLDER = "saved_timelines"
os.makedirs(SAVE_FOLDER, exist_ok=True)

def save_timelines(filename):
    if not filename.endswith(".json"):
        filename += ".json"

    data = {
        "song_timeline": song_timeline,
        "voice_timeline": voice_timeline
    }
    filepath = os.path.join(SAVE_FOLDER, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    return f"✅ Timelines saved to {filepath}"

def list_saved_timelines():
    return [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".json")]

def load_timelines(filename):
    filepath = os.path.join(SAVE_FOLDER, filename)
    if not os.path.exists(filepath):
        return "❌ Save file not found."

    with open(filepath, "r") as f:
        data = json.load(f)

    song_timeline.clear()
    song_timeline.extend(data.get("song_timeline", []))

    voice_timeline.clear()
    voice_timeline.extend(data.get("voice_timeline", []))

    return f"✅ Timelines loaded from {filepath}"
