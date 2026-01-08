import torch
from transformers import AlbertTokenizer, AlbertForSequenceClassification
import re
from .config import Config

# Global model & tokenizer
tokenizer = None
model = None
device = "cpu"  

# Vulgar words (expand as needed)
VULGAR_WORDS = [
    "fuck", "shit", "bitch", "asshole", "cunt", "nigger", "faggot",
    "damn", "bastard", "whore", "slut", "dick", "pussy", "cock"
]
VULGAR_PATTERN = re.compile(r'\b(' + '|'.join(map(re.escape, VULGAR_WORDS)) + r')\b', re.IGNORECASE)

LABELS = ["toxicity", "threat", "insult", "sexual_explicit", "obscene"]

def load_model():
    global tokenizer, model
    print("Loading ALBERT toxicity model from ./albert_toxicity_moderator ...")
    tokenizer = AlbertTokenizer.from_pretrained(Config.MODEL_PATH)
    model = AlbertForSequenceClassification.from_pretrained(Config.MODEL_PATH)
    model.eval()
    print("Model loaded successfully!")

def moderate_text(text: str) -> dict:
    text = text.strip()

    # 1. Vulgar word check
    if VULGAR_PATTERN.search(text):
        return {
            "safe": False,
            "reason": "vulgar_language",
            "message": "Blocked: contains prohibited vulgar word(s)",
            "scores": None
        }

    # 2. ALBERT inference
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.sigmoid(logits).cpu().numpy()[0]

    scores = {label: float(prob) for label, prob in zip(LABELS, probs)}
    is_toxic = any(prob > 0.5 for prob in probs)

    return {
        "safe": not is_toxic,
        "reason": "toxic_content" if is_toxic else "safe",
        "message": "Blocked: toxic content detected" if is_toxic else "Safe to post",
        "scores": scores if is_toxic else None
    }