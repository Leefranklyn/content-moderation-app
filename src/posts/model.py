from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, ObjectIdField
from ..user.model import User
from datetime import datetime

class Post(Document):
    content = StringField(required=True)
    author = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    # comments = ListField(ReferenceField('Comment'))
    likes = ListField(ReferenceField(User))      
    dislikes = ListField(ReferenceField(User))

    meta = {'collection': 'posts', 'ordering': ['-created_at']}