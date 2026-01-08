from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, ObjectIdField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    meta = {'collection': 'users'}

class Post(Document):
    content = StringField(required=True)
    author = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    # comments = ListField(ReferenceField('Comment'))
    likes = ListField(ReferenceField(User))      # Users who liked
    dislikes = ListField(ReferenceField(User))   # Users who disliked

    meta = {'collection': 'posts', 'ordering': ['-created_at']}

class Comment(Document):
    content = StringField(required=True)
    author = ReferenceField(User, required=True)
    post = ReferenceField(Post, required=True)
    parent = ReferenceField("self", null=True)
    likes = ListField(ReferenceField(User))      # Users who liked
    dislikes = ListField(ReferenceField(User))   # Users who disliked
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'comments'}