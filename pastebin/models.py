import datetime

from app import db

from authentication.models import User


CATEGORIES = (
    'None', 'Cryptocurrency', 'Cybersecurity', 'Fixit', 'Food', 'Gaming', 'Haiku', 'Help',
    'History', 'Housing', 'Jokes', 'Legal', 'Money', 'Movies', 'Music', 'Pets', 'Photo',
    'Science', 'Software', 'Source Code', 'Spirit', 'Sports', 'Travel', 'TV', 'Writing',
)

PASTE_EXPIRATION = (
    (0, 'Never'), (3600, '1 Hour'), (86400, '1 Day'), (2592000, '1 Month'), (31104000, '1 Year'),
)

PASTE_EXPOSURE = (
    'Public', 'Unlisted', 'Private',
)


class Comment(db.EmbeddedDocument):
    content = db.StringField(max_length=300, required=True)
    author = db.ReferenceField(User, reverse_delete_rule=db.CASCADE)

    created = db.DateTimeField()
    updated = db.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Comment, self).save(*args, **kwargs)

    def __repr__(self):
        if len(str(self.content)) > 50:
            return f"Comment {self.author} - {str(self.content)[:50].strip()}.."
        return f"Comment {self.author} - {str(self.content)}"


class Paste(db.Document):
    content = db.StringField(max_length=512000, required=True)

    category = db.StringField(choices=CATEGORIES, required=False, default='None')
    tags = db.StringField(max_length=25, required=False)
    paste_expiration = db.IntegerField(choices=PASTE_EXPIRATION, required=True, default=0)
    paste_exposure = db.StringField(choices=PASTE_EXPOSURE, required=True, default='Public')
    paste_name = db.StringField(max_length=50, required=False)

    author = db.ReferenceField(User, reverse_delete_rule=db.CASCADE)
    comments = db.ReferenceField(Comment, reverse_delete_rule=db.CASCADE)

    created = db.DateTimeField()
    updated = db.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Paste, self).save(*args, **kwargs)

    def __repr__(self):
        if len(str(self.content)) > 50:
            return f"Paste {self.author} - {str(self.content)[:50].strip()}.."
        return f"Paste {self.author} - {str(self.content)}"
