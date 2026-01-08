from fastapi import HTTPException
from .model import User
from ..utils.auth import create_access_token
from ..utils.security import hash_password, verify_password


def register_user(username: str, password: str):
    if User.objects(username=username).first():
        raise HTTPException(status_code=400, detail="Username taken")
    hashed_password = hash_password(password)
    
    User(username=username, password=hashed_password).save()
    return {"message": "User registered successfully"}

def login_user(username: str, password: str):
    user = User.objects(username=username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(str(user.id))
    
    return {
        "success": True,
        "message": "User Login Successful",
        "user": {"id": str(user.id), "username": user.username},
        "token": token
    }

def get_current_loggedIn_user_profile(current_user):
    if user := User.objects(id=current_user.id).first():
        return {
            "id": str(user.id),
            "username": user.username,
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")