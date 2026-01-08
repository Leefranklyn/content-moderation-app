from fastapi import APIRouter, Depends
from typing import List
from ..utils.auth import get_current_user
from ..schemas import UserCreate
from .services import register_user, login_user, get_current_loggedIn_user_profile
from .model import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register(user: UserCreate):
    return register_user(user.username, user.password)

@router.post("/login")
def login(user: UserCreate):
    return login_user(user.username, user.password)

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return get_current_loggedIn_user_profile(current_user)
