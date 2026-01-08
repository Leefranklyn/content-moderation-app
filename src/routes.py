from fastapi import APIRouter, Depends
from typing import List

from utils.auth import get_current_user
from .schemas import UserCreate, PostResponse, CommentResponse, PostCreate, CommentCreate
from .services import dislike_comment, dislike_post, get_comments_for_post, get_current_loggedIn_user_profile, get_post_by_id, get_replies_for_comment, like_comment, like_post, login_user, register_user, create_new_post, create_new_comment, get_all_posts
from .models import User
router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    return register_user(user.username, user.password)

@router.post("/login")
def login(user: UserCreate):
    return login_user(user.username, user.password)

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return get_current_loggedIn_user_profile(current_user)

@router.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, current_user: User = Depends(get_current_user)):
    
    db_post = create_new_post(content = post.content, post_author = current_user)
    
    return PostResponse(
        id=str(db_post.id),
        content=db_post.content,
        author=str(current_user.id),
        author_name=current_user.username,
        created_at=db_post.created_at,
        comments=[]
    )

@router.post("/comments", response_model=CommentResponse)
def create_comment(comment: CommentCreate, current_user: User = Depends(get_current_user)):
    db_comment = create_new_comment(content = comment.content, post_author = current_user, post_id = comment.post_id, parent_comment_id=comment.parent_comment_id)
    return CommentResponse(
        id=str(db_comment.id),
        content=db_comment.content,
        author=str(current_user.id),
        author_name=current_user.username,
        created_at=db_comment.created_at
    )

@router.get("/posts", response_model=List[PostResponse])
def get_posts():
    posts = get_all_posts()
    response = []

    for p in posts:
        comments = get_comments_for_post(p.id)

        response.append(
            PostResponse(
                id=str(p.id),
                content=p.content,
                author=p.author.username,
                created_at=p.created_at,
                likes=len(p.likes) if hasattr(p, "likes") else 0,
                dislikes=len(p.dislikes) if hasattr(p, "dislikes") else 0,
                comments=[
                    CommentResponse(
                        id=str(c.id),
                        content=c.content,
                        author=c.author.username,
                        created_at=c.created_at,
                        likes=len(c.likes) if hasattr(c, "likes") else 0,
                        dislikes=len(c.dislikes) if hasattr(c, "dislikes") else 0,
                    ) for c in comments
                ]
            )
        )

    return response

@router.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: str):
    post = get_post_by_id(post_id)
    comments = get_comments_for_post(post_id)

    return PostResponse(
        id=str(post.id),
        content=post.content,
        author=str(post.author.id),
        author_name=post.author.username,
        created_at=post.created_at,
        likes=len(post.likes) if hasattr(post, "likes") else 0,
        dislikes=len(post.dislikes) if hasattr(post, "dislikes") else 0,
        comments=[
            CommentResponse(
                id=str(c.id),
                content=c.content,
                author=str(c.author.id),
                author_name=c.author.username,
                created_at=c.created_at,
                likes=len(c.likes) if hasattr(c, "likes") else 0,
                dislikes=len(c.dislikes) if hasattr(c, "dislikes") else 0,
            ) for c in comments
        ]
    )

@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
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

@router.get("/comments/{comment_id}/replies", response_model=List[CommentResponse])
def fetch_comment_replies(comment_id: str):
    replies = get_replies_for_comment(comment_id)

    return [
        CommentResponse(
            id=str(r.id),
            content=r.content,
            author=r.author.username,
            created_at=r.created_at,
            likes=len(r.likes) if hasattr(r, "likes") else 0,
            dislikes=len(r.dislikes) if hasattr(r, "dislikes") else 0,
        )
        for r in replies
    ]

@router.post("/posts/{post_id}/like")
def like_post_route(post_id: str, current_user: User = Depends(get_current_user)):
    post = like_post(post_id, current_user)
    return {"likes": len(post.likes), "dislikes": len(post.dislikes)}

@router.post("/posts/{post_id}/dislike")
def dislike_post_route(post_id: str, current_user: User = Depends(get_current_user)):
    post = dislike_post(post_id, current_user)
    return {"likes": len(post.likes), "dislikes": len(post.dislikes)}

@router.post("/comments/{comment_id}/like")
def like_comment_route(comment_id: str, current_user: User = Depends(get_current_user)):
    comment = like_comment(comment_id, current_user)
    return {"likes": len(comment.likes), "dislikes": len(comment.dislikes)}

@router.post("/comments/{comment_id}/dislike")
def dislike_comment_route(comment_id: str, current_user: User = Depends(get_current_user)):
    comment = dislike_comment(comment_id, current_user)
    return {"likes": len(comment.likes), "dislikes": len(comment.dislikes)}

@router.get("/")
def root():
    return {"message": "SafeSocial API - ALBERT Moderated Chat"}