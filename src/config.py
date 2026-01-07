import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODEL_PATH = os.getenv("TRAINED_MODEL_PATH")
    DATABASE_URL = os.getenv("DATABASE_URL")