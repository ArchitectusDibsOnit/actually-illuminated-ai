# dynamic_model_loader.py

from audiocraft.models import MusicGen

def list_available_models():
    return ["facebook/musicgen-small", "facebook/musicgen-medium", "facebook/musicgen-large"]

def load_music_model(model_name):
    print(f"[🎛️] Loading {model_name}...")
    model = MusicGen.get_pretrained(model_name)
    print(f"✅ {model_name} loaded successfully.")
    return model
