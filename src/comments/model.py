from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, ObjectIdField
from ..user.model import User
from ..posts.model import Post
from datetime import datetime

class Comment(Document):
    content = StringField(required=True)
    author = ReferenceField(User, required=True)
    post = ReferenceField(Post, required=True)
    parent = ReferenceField("self", null=True)
    likes = ListField(ReferenceField(User))
    dislikes = ListField(ReferenceField(User)) 
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'comments'}