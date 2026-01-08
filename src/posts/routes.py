from fastapi import APIRouter, Depends
from typing import List
from ..utils.auth import get_current_user
from ..schemas import PostCreate, PostResponse, CommentResponse
from .services import create_new_post, get_all_posts, get_post_by_id, like_post, dislike_post, edit_post
from ..comments.services import get_comments_for_post
from ..user.model import User

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("", response_model=PostResponse)
def create_post(post: PostCreate, current_user: User = Depends(get_current_user)):
    db_post = create_new_post(content=post.content, post_author=current_user)
    return PostResponse(
        id=str(db_post.id),
        content=db_post.content,
        author=str(current_user.id),
        author_name=current_user.username,
        created_at=db_post.created_at,
        comments=[],
        likes=len(db_post.likes),
        dislikes=len(db_post.dislikes)
    )

@router.get("", response_model=List[PostResponse])
def get_posts():
    posts = get_all_posts()
    response = []

    for p in posts:
        comments = get_comments_for_post(p.id)
        response.append(
            PostResponse(
                id=str(p.id),
                content=p.content,
                author=str(p.author.id),
                author_name=p.author.username,
                created_at=p.created_at,
                likes=len(p.likes),
                dislikes=len(p.dislikes),
                comments=[
                    CommentResponse(
                        id=str(c.id),
                        content=c.content,
                        author=str(c.author.id),
                        author_name=c.author.username,
                        created_at=c.created_at,
                        likes=len(c.likes),
                        dislikes=len(c.dislikes),
                        replies=[]
                    )
                    for c in comments
                ]
            )
        )
    return response

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: str):
    post = get_post_by_id(post_id)
    comments = get_comments_for_post(post_id)

    return PostResponse(
        id=str(post.id),
        content=post.content,
        author=str(post.author.id),
        author_name=post.author.username,
        created_at=post.created_at,
        likes=len(post.likes),
        dislikes=len(post.dislikes),
        comments=[
            CommentResponse(
                id=str(c.id),
                content=c.content,
                author=str(c.author.id),
                author_name=c.author.username,
                created_at=c.created_at,
                likes=len(c.likes),
                dislikes=len(c.dislikes),
                replies=[]
            ) for c in comments
        ]
    )
    
@router.get("/{post_id}/comments", response_model=List[CommentResponse])
def fetch_post_comments(post_id: str):
    comments = get_comments_for_post(post_id)

    return [
        CommentResponse(
            id=str(c.id),
            content=c.content,
            author=c.author.username,
            created_at=c.created_at,
            likes=len(c.likes) if hasattr(c, "likes") else 0,
            dislikes=len(c.dislikes) if hasattr(c, "dislikes") else 0,
        )
        for c in comments
    ]

@router.patch("/{post_id}", response_model=PostResponse)
def edit_post_route(post_id: str, new_content: str, current_user: User = Depends(get_current_user)):
    post = edit_post(post_id, new_content, current_user)

    comments = get_comments_for_post(post.id)
    return PostResponse(
        id=str(post.id),
        content=post.content,
        author=str(post.author.id),
        author_name=post.author.username,
        created_at=post.created_at,
        likes=len(post.likes),
        dislikes=len(post.dislikes),
        comments=[
            CommentResponse(
                id=str(c.id),
                content=c.content,
                author=str(c.author.id),
                author_name=c.author.username,
                created_at=c.created_at,
                likes=len(c.likes),
                dislikes=len(c.dislikes),
                replies=[]
            )
            for c in comments
        ]
    )

# Likes & Dislikes
@router.post("/{post_id}/like")
def like_post_route(post_id: str, current_user: User = Depends(get_current_user)):
    post = like_post(post_id, current_user)
    return {"likes": len(post.likes), "dislikes": len(post.dislikes)}

@router.post("/{post_id}/dislike")
def dislike_post_route(post_id: str, current_user: User = Depends(get_current_user)):
    post = dislike_post(post_id, current_user)
    return {"likes": len(post.likes), "dislikes": len(post.dislikes)}
