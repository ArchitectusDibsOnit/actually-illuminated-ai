# project_manager.py

import os
import json
from datetime import datetime

PROJECTS_DIR = "saved_projects"

if not os.path.exists(PROJECTS_DIR):
    os.makedirs(PROJECTS_DIR)

def save_project(project_name, data):
    """Saves a dictionary of session state into a timestamped JSON file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_name = project_name.replace(" ", "_").replace("/", "-")
    project_folder = os.path.join(PROJECTS_DIR, safe_name)
    os.makedirs(project_folder, exist_ok=True)

    file_path = os.path.join(project_folder, f"session_{timestamp}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return file_path

def load_project(project_name, session_file=None):
    """Loads the most recent or a specific session file."""
    safe_name = project_name.replace(" ", "_").replace("/", "-")
    project_folder = os.path.join(PROJECTS_DIR, safe_name)
    if not os.path.exists(project_folder):
        raise FileNotFoundError(f"No such project: {project_name}")

    sessions = sorted([
        f for f in os.listdir(project_folder)
        if f.startswith("session_") and f.endswith(".json")
    ])

    if not sessions:
        raise FileNotFoundError("No session files found in this project.")

    if session_file:
        target_file = session_file
    else:
        target_file = sessions[-1]  # most recent

    file_path = os.path.join(project_folder, target_file)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_projects():
    return [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]

def list_sessions(project_name):
    safe_name = project_name.replace(" ", "_").replace("/", "-")
    project_folder = os.path.join(PROJECTS_DIR, safe_name)
    return sorted([
        f for f in os.listdir(project_folder)
        if f.startswith("session_") and f.endswith(".json")
    ]) if os.path.exists(project_folder) else []
