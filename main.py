from transformers import AlbertTokenizer, AlbertForSequenceClassification
import os
from dotenv import load_dotenv

load_dotenv()

tokenizer = AlbertTokenizer.from_pretrained(os.getenv("TRAINED_MODEL_PATH"))
model = AlbertForSequenceClassification.from_pretrained(os.getenv("TRAINED_MODEL_PATH"))
# Quick test
inputs = tokenizer("You idiot", return_tensors="pt")
print(model(**inputs).logits)