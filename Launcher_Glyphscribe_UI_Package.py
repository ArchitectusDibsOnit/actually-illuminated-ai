import os
import subprocess

def launch_ai_system():
    print("\n💡 Launching Actually Illuminated AI...")
    os.system("python actually_illuminated_ai.py")


def update_ai_system():
    print("\n⬆️ Checking for updates...")
    # Simulated update process
    if os.path.exists("updates/update_version.txt"):
        with open("updates/update_version.txt", "r") as f:
            update_version = f.read().strip()
            print(f"\n✨ Update found: {update_version} ready to install.")
    else:
        print("\n🚫 No updates found.")


def display_launcher_menu():
    while True:
        print("\n=== Actually Illuminated AI Launcher ===")
        print("1. Launch AI System")
        print("2. Check for Updates")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            launch_ai_system()
        elif choice == '2':
            update_ai_system()
        elif choice == '3':
            print("\n👋 Exiting launcher.")
            break
        else:
            print("\n⚠️ Invalid option. Please try again.")


if __name__ == "__main__":
    display_launcher_menu()


# 🪶 Glyphscribe (Cleaned)
import json

glyphscribe_database = "glyphscribe.json"


def load_glyphscribe():
    if os.path.exists(glyphscribe_database):
        with open(glyphscribe_database, 'r') as file:
            return json.load(file)
    else:
        return {}


def save_glyphscribe(glyphs):
    with open(glyphscribe_database, 'w') as file:
        json.dump(glyphs, file, indent=4)


def add_glyphscribe_entry(glyph_name, glyph_data):
    glyphs = load_glyphscribe()
    glyphs[glyph_name] = glyph_data
    save_glyphscribe(glyphs)


print("\n📝 Glyphscribe module loaded successfully.")
