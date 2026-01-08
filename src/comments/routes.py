from fastapi import APIRouter, Depends
from typing import List
from ..utils.auth import get_current_user
from ..schemas import CommentCreate, CommentResponse
from .services import create_new_comment, get_replies_for_comment, edit_comment, like_comment, dislike_comment
from ..user.model import User

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("", response_model=CommentResponse)
def create_comment(comment: CommentCreate, current_user: User = Depends(get_current_user)):
    db_comment = create_new_comment(
        content=comment.content,
        post_author=current_user,
        post_id=comment.post_id,
        parent_comment_id=comment.parent_comment_id
    )
    return CommentResponse(
        id=str(db_comment.id),
        content=db_comment.content,
        author=str(current_user.id),
        author_name=current_user.username,
        created_at=db_comment.created_at,
        likes=len(db_comment.likes),
        dislikes=len(db_comment.dislikes),
        replies=[]
    )

@router.get("/{comment_id}/replies", response_model=List[CommentResponse])
def fetch_comment_replies(comment_id: str):
    replies = get_replies_for_comment(comment_id)
    return [
        CommentResponse(
            id=str(r.id),
            content=r.content,
            author=str(r.author.id),
            author_name=r.author.username,
            created_at=r.created_at,
            likes=len(r.likes),
            dislikes=len(r.dislikes),
            replies=[]
        )
        for r in replies
    ]
    
@router.put("/{comment_id}", response_model=CommentResponse)
def edit_comment_route(comment_id: str, new_content: str, current_user: User = Depends(get_current_user)):
    comment = edit_comment(comment_id, new_content, current_user)

    return CommentResponse(
        id=str(comment.id),
        content=comment.content,
        author=str(comment.author.id),
        author_name=comment.author.username,
        created_at=comment.created_at,
        likes=len(comment.likes),
        dislikes=len(comment.dislikes),
        replies=[]
    )

# Likes & Dislikes
@router.post("/{comment_id}/like")
def like_comment_route(comment_id: str, current_user: User = Depends(get_current_user)):
    comment = like_comment(comment_id, current_user)
    return {"likes": len(comment.likes), "dislikes": len(comment.dislikes)}

@router.post("/{comment_id}/dislike")
def dislike_comment_route(comment_id: str, current_user: User = Depends(get_current_user)):
    comment = dislike_comment(comment_id, current_user)
    return {"likes": len(comment.likes), "dislikes": len(comment.dislikes)}
