# emotion_detector.py (HuggingFace + Fallback)

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import text2emotion as te

model_name = "cardiffnlp/twitter-roberta-base-emotion"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
labels = ['anger', 'joy', 'optimism', 'sadness']

def detect_emotion(text):
    try:
        inputs = tokenizer(text, return_tensors="pt")
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=-1)[0].tolist()
        ranked = sorted(zip(labels, scores), key=lambda x: x[1], reverse=True)
        return ranked[0][0].capitalize()
    except Exception:
        fallback = te.get_emotion(text)
        return max(fallback, key=fallback.get).capitalize()
