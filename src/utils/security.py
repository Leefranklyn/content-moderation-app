import hashlib
import bcrypt

def hash_password(password: str) -> str:
    prehashed = hashlib.sha256(password.encode("utf-8")).digest()  
    return bcrypt.hashpw(prehashed, bcrypt.gensalt(rounds=12)).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    prehashed = hashlib.sha256(plain_password.encode("utf-8")).digest()
    return bcrypt.checkpw(prehashed, hashed_password.encode("utf-8"))