from .moderation import load_model, moderate_text
from fastapi import APIRouter
from .user.routes import router as users_router
from .posts.routes import router as posts_router
from .comments.routes import router as comments_router

router = APIRouter()
router.include_router(users_router)
router.include_router(posts_router)
router.include_router(comments_router)

@router.get("/")
def root():
    return {"message": "SafeSocial API - ALBERT Moderated Chat"}
