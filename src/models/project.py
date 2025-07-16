from mongoengine import Document, StringField, DateField, DateTimeField, ReferenceField
from datetime import datetime, timezone
from .user import User

class Project(Document):
    name = StringField(required=True, max_length=100)
    description = StringField(required=False, max_length=500)
    dueDate = DateField(required=True)
    status = StringField(required=True, choices=["not-started", "in-progress", "completed"])
    imageId = StringField(required=False, max_length=100)
    imageUrl = StringField(required=False, max_length=200)
    owner = ReferenceField(User, required=False)
    createdAt = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updatedAt = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'projects'
    }

    def save(self, *args, **kwargs):
        if not self.createdAt:
            self.createdAt = datetime.now(timezone.utc)
        self.updatedAt = datetime.now(timezone.utc)
        return super(Project, self).save(*args, **kwargs)

    def to_json(self):
        return {
            "id": str(self.id), 
            "name": self.name, 
            "description": self.description, 
            "dueDate": self.dueDate.isoformat() if self.dueDate else None, 
            "status": self.status, 
            "imageId": self.imageId, 
            "imageUrl": self.imageUrl,
            "owner": {
                "id": str(self.owner.id),
                "name": self.owner.name,
                "email": self.owner.email
            } if self.owner else None,
            "createdAt": self.createdAt.isoformat() if self.createdAt else None,
            "updatedAt": self.updatedAt.isoformat() if self.updatedAt else None
        }
