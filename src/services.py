from fastapi import HTTPException, Depends
from utils.auth import create_access_token, get_current_user
from utils.security import hash_password, verify_password
from .models import User, Post, Comment
from .moderation import moderate_text
from mongoengine.errors import DoesNotExist

def register_user(username: str, password: str):
    if User.objects(username=username).first():
        raise HTTPException(status_code=400, detail="Username taken")
    hashed_password = hash_password(password)
    
    User(username=username, password=hashed_password).save()
    return {"message": "User registered successfully"}

def login_user(username: str, password: str):
    user = User.objects(username=username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(str(user.id))
    
    return {
        "success": True,
        "message": "User Login Successful",
        "user": {"id": str(user.id), "username": user.username},  # add whatever you need
        "token": token
    }

def get_current_loggedIn_user_profile(current_user):
    if user := User.objects(id=current_user.id).first():
        return {
            "id": str(user.id),
            "username": user.username,
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")

def create_new_post(content: str, post_author: User):
    result = moderate_text(content)
    if not result["safe"]:
        raise HTTPException(status_code=400, detail=result)

    post = Post(content=content, author=post_author)
    post.save()
    return post

def create_new_comment(
    content: str,
    post_author: User,
    post_id: str,
    parent_comment_id: str | None = None
):
    try:
        post = Post.objects.get(id=post_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

    parent_comment = None
    if parent_comment_id:
        try:
            parent_comment = Comment.objects.get(id=parent_comment_id)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Parent comment not found")

    result = moderate_text(content)
    if not result["safe"]:
        raise HTTPException(status_code=400, detail=result)

    comment = Comment(
        content=content,
        author=post_author,
        post=post,
        parent=parent_comment
    )
    comment.save()

    return comment


def get_all_posts():
    posts = Post.objects().select_related()
    return posts

def get_post_by_id(post_id: str):
    try:
        post = Post.objects.get(id=post_id)
        return post
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")
    
def get_comments_for_post(post_id: str):
    try:
        post = Post.objects.get(id=post_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return (
        Comment.objects(post=post, parent=None)
        .order_by("+created_at")   # oldest first — or "-created_at" for newest
        .select_related()          # pre-fetch author
    )

def get_replies_for_comment(comment_id: str):
    try:
        parent = Comment.objects.get(id=comment_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Comment not found")

    return Comment.objects(parent=parent).select_related()

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

def edit_comment(comment_id: str, new_content: str, current_user: User):
    try:
        comment = Comment.objects.get(id=comment_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.author.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    result = moderate_text(new_content)
    if not result["safe"]:
        raise HTTPException(status_code=400, detail=result)

    comment.content = new_content
    comment.save()
    return comment

def like_post(post_id: str, user: User):
    try:
        post = Post.objects.get(id=post_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

    if user in post.likes:
        post.likes.remove(user)  # toggle off
    else:
        post.likes.append(user)
        if user in post.dislikes:
            post.dislikes.remove(user)  # remove opposite vote

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


def like_comment(comment_id: str, user: User):
    try:
        comment = Comment.objects.get(id=comment_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Comment not found")

    if user in comment.likes:
        comment.likes.remove(user)
    else:
        comment.likes.append(user)
        if user in comment.dislikes:
            comment.dislikes.remove(user)

    comment.save()
    return comment

def dislike_comment(comment_id: str, user: User):
    try:
        comment = Comment.objects.get(id=comment_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Comment not found")

    if user in comment.dislikes:
        comment.dislikes.remove(user)
    else:
        comment.dislikes.append(user)
        if user in comment.likes:
            comment.likes.remove(user)

    comment.save()
    return comment
