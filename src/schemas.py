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
    parent_comment_id: Optional[str] = None  # <--- Add this

class CommentResponse(BaseModel):
    id: str
    content: str
    author: str
    # author_name: str
    created_at: datetime
    likes: Optional[int] = 0
    dislikes: Optional[int] = 0
    replies: Optional[List['CommentResponse']] = []

class PostResponse(BaseModel):
    id: str
    content: str
    author: str
    # author_name: str
    created_at: datetime
    likes: Optional[int] = 0
    dislikes: Optional[int] = 0
    comments: List[CommentResponse] = []

class ModerationResponse(BaseModel):
    safe: bool
    reason: str
    message: str
    scores: Optional[dict] = None