from fastapi import HTTPException
from .models import User, Post, Comment
from .moderation import moderate_text
from mongoengine.errors import DoesNotExist

def register_user(username: str):
    if User.objects(username=username).first():
        raise HTTPException(status_code=400, detail="Username taken")
    User(username=username).save()
    return {"message": "User registered successfully"}

def create_new_post(content: str, author: str):
    if not User.objects(username=author).first():
        raise HTTPException(status_code=404, detail="User not found")

    result = moderate_text(content)
    if not result["safe"]:
        raise HTTPException(status_code=400, detail=result)

    post = Post(content=content, author=author)
    post.save()
    return post

def create_new_comment(content: str, author: str, post_id: str):
    if not User.objects(username=author).first():
        raise HTTPException(status_code=404, detail="User not found")

    try:
        parent_post = Post.objects.get(id=post_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

    result = moderate_text(content)
    if not result["safe"]:
        raise HTTPException(status_code=400, detail=result)

    comment = Comment(content=content, author=author, post=parent_post)
    comment.save()

    parent_post.comments.append(comment)
    parent_post.save()

    return comment

def get_all_posts():
    posts = Post.objects()
    return posts