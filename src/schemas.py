from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
class PostCreate(BaseModel):
    content: str

class CommentCreate(BaseModel):
    content: str
    post_id: str

class CommentResponse(BaseModel):
    id: str
    content: str
    author: str
    # author_name: str
    created_at: datetime

class PostResponse(BaseModel):
    id: str
    content: str
    author: str
    # author_name: str
    created_at: datetime
    comments: List[CommentResponse] = []

class ModerationResponse(BaseModel):
    safe: bool
    reason: str
    message: str
    scores: Optional[dict] = None