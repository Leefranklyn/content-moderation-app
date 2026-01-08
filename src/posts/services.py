from fastapi import HTTPException
from ..user.model import User
from ..moderation import moderate_text
from .model import Post
from mongoengine.errors import DoesNotExist


def create_new_post(content: str, post_author: User):
    result = moderate_text(content)
    if not result["safe"]:
        raise HTTPException(status_code=400, detail=result)

    post = Post(content=content, author=post_author)
    post.save()
    return post

def get_all_posts():
    posts = Post.objects().select_related()
    return posts

def get_post_by_id(post_id: str):
    try:
        post = Post.objects.get(id=post_id)
        return post
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")
    
def like_post(post_id: str, user: User):
    try:
        post = Post.objects.get(id=post_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

    if user in post.likes:
        post.likes.remove(user)  
    else:
        post.likes.append(user)
        if user in post.dislikes:
            post.dislikes.remove(user)

    post.save()
    return post

def edit_post(post_id: str, new_content: str, current_user: User):
    try:
        post = Post.objects.get(id=post_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    result = moderate_text(new_content)
    if not result["safe"]:
        raise HTTPException(status_code=400, detail=result)

    post.content = new_content
    post.save()
    return post

def dislike_post(post_id: str, user: User):
    try:
        post = Post.objects.get(id=post_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

    if user in post.dislikes:
        post.dislikes.remove(user)
    else:
        post.dislikes.append(user)
        if user in post.likes:
            post.likes.remove(user)

    post.save()
    return post