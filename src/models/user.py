from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime, timezone

class User(Document):
    name = StringField(required=True, max_length=50)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    createdAt = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updatedAt = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'users'
    }

    def save(self, *args, **kwargs):
        if not self.createdAt:
            self.createdAt = datetime.now(timezone.utc)
        self.updatedAt = datetime.now(timezone.utc)
        return super(User, self).save(*args, **kwargs)

    def to_json(self):
        return {
            "id": str(self.id), 
            "name": self.name, 
            "email": self.email,
            "createdAt": self.createdAt.isoformat() if self.createdAt else None,
            "updatedAt": self.updatedAt.isoformat() if self.updatedAt else None
        }
