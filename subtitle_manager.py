# subtitle_manager.py (Emotion Detection + Auto .srt Save + JSON Export)

import os
import whisper
import json
from subtitle_exporter import export_subtitles

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

try:
    tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-emotion")
    model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-emotion")
    hf_emotion_available = True
except Exception as e:
    print("[!] HuggingFace emotion model unavailable, falling back to text2emotion.")
    import text2emotion as t2e
    hf_emotion_available = False

whisper_model = whisper.load_model("base")

SUBTITLE_DIR = "subtitles"
os.makedirs(SUBTITLE_DIR, exist_ok=True)

def transcribe_audio(audio_path):
    """Returns transcribed text and Whisper segments."""
    result = whisper_model.transcribe(audio_path)
    return result["text"], result.get("segments", [])

def save_subtitles(text, audio_filename, segments=None):
    base_name = os.path.splitext(audio_filename)[0]
    txt_path = os.path.join(SUBTITLE_DIR, f"{base_name}_subtitles.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    if segments:
        timeline_log = convert_segments_to_srt_format(segments)
        export_subtitles(text, timeline_log, base_name, format="srt")
        json_path = os.path.join(SUBTITLE_DIR, f"{base_name}_segments.json")
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(timeline_log, jf, indent=2)

def get_subtitles(audio_filename):
    base_name = os.path.splitext(audio_filename)[0]
    subtitle_path = os.path.join(SUBTITLE_DIR, f"{base_name}_subtitles.txt")
    if os.path.exists(subtitle_path):
        with open(subtitle_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def auto_generate_phonemes(text, text_to_phonemes_func):
    return text_to_phonemes_func(text)

def convert_segments_to_srt_format(segments, voice="Default"):
    """Converts Whisper segments to a subtitle_exporter-compatible format."""
    timeline_log = []
    for seg in segments:
        emotion = detect_emotion(seg["text"])
        timeline_log.append({
            "start_time": seg["start"],
            "end_time": seg["end"],
            "voice": voice,
            "lyrics": seg["text"],
            "emotion": emotion
        })
    return timeline_log

def detect_emotion(text):
    text = text.strip()
    if not text:
        return "Neutral"

    if hf_emotion_available:
        inputs = tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits
        probs = torch.nn.functional.softmax(logits, dim=1)[0]
        emotion_id = torch.argmax(probs).item()
        label = model.config.id2label[emotion_id]
        return label.capitalize()
    else:
        emo_dict = t2e.get_emotion(text)
        if emo_dict:
            return max(emo_dict, key=emo_dict.get)
        return "Neutral"
