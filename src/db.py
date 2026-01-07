from mongoengine import connect
from .config import Config

def init_db():
    connect(host=Config.DATABASE_URL)
    print("Connected to MongoDB")