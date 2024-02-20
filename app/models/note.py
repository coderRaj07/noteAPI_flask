from app import db
from datetime import datetime

class Note(db.Document):
    title = db.StringField(required=True)
    content = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)
    owner = db.ReferenceField('User')
    shared_with = db.ListField(db.ReferenceField('User'))
