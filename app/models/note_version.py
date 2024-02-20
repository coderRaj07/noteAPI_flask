from app import db
from datetime import datetime

class NoteVersion(db.Document):
    note = db.ReferenceField('Note')
    user = db.ReferenceField('User')
    changes = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'note_versions'}
