from fastapi import APIRouter
from typing import List
from .schemas import UserCreate, PostResponse, CommentResponse, PostCreate, CommentCreate
from .services import login_user, register_user, create_new_post, create_new_comment, get_all_posts

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    return register_user(user.username, user.password)

@router.post("/login")
def login(user: UserCreate):
    return login_user(user.username, user.password)

@router.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate):
    db_post = create_new_post(post.content, post.author)
    return PostResponse(
        id=str(db_post.id),
        content=db_post.content,
        author=db_post.author,
        created_at=db_post.created_at,
        comments=[]
    )

@router.post("/comments", response_model=CommentResponse)
def create_comment(comment: CommentCreate):
    db_comment = create_new_comment(comment.content, comment.author, comment.post_id)
    return CommentResponse(
        id=str(db_comment.id),
        content=db_comment.content,
        author=db_comment.author,
        created_at=db_comment.created_at
    )

@router.get("/posts", response_model=List[PostResponse])
def get_posts():
    db_posts = get_all_posts()
    response = []
    for p in db_posts:
        comments = [
            CommentResponse(
                id=str(c.id),
                content=c.content,
                author=c.author,
                created_at=c.created_at
            ) for c in p.comments
        ]
        response.append(PostResponse(
            id=str(p.id),
            content=p.content,
            author=p.author,
            created_at=p.created_at,
            comments=comments
        ))
    return response

@router.get("/")
def root():
    return {"message": "SafeSocial API - ALBERT Moderated Chat"}