from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    meta = {'collection': 'users'}

class Post(Document):
    content = StringField(required=True)
    author = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    comments = ListField(ReferenceField('Comment'))

    meta = {'collection': 'posts', 'ordering': ['-created_at']}

class Comment(Document):
    content = StringField(required=True)
    author = StringField(required=True)
    post = ReferenceField(Post, required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'comments'}