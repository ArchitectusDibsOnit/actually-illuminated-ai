# memory_manager.py

import os
import json

USER_PREFS_FILE = "user_preferences.json"

def load_user_preferences():
    if os.path.exists(USER_PREFS_FILE):
        try:
            with open(USER_PREFS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_user_preferences(prefs):
    try:
        with open(USER_PREFS_FILE, "w") as f:
            json.dump(prefs, f, indent=4)
    except Exception as e:
        print(f"⚠️ Failed to save user preferences: {e}")
