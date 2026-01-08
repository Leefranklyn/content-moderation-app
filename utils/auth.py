# utils/auth.py
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from mongoengine.errors import DoesNotExist
from src.config import Config
from src.models import User
from utils.security import verify_password  

SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_HOURS = Config.ACCESS_TOKEN_EXPIRE_HOURS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # for OpenAPI docs

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=int(ACCESS_TOKEN_EXPIRE_HOURS)))
    to_encode = {"exp": expire, "sub": user_id}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[str(ALGORITHM)])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    try:
        user = User.objects.get(id=user_id)
    except DoesNotExist:
        raise credentials_exception

    return user