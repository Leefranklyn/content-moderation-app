from fastapi import HTTPException
from .model import Comment
from ..moderation import moderate_text
from ..posts.model import Post
from ..user.model import User
from mongoengine.errors import DoesNotExist


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

def get_comments_for_post(post_id: str):
    try:
        post = Post.objects.get(id=post_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return (
        Comment.objects(post=post, parent=None)
        .order_by("+created_at")   
        .select_related()
    )
    
def get_replies_for_comment(comment_id: str):
    try:
        parent = Comment.objects.get(id=comment_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Comment not found")

    return Comment.objects(parent=parent).select_related()

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