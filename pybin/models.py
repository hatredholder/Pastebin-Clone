import datetime
import uuid

from app import db

import pybin.choices as choices


class Comment(db.EmbeddedDocument):
    content = db.StringField(max_length=300, required=True)
    author = db.ReferenceField("User", required=True)
    paste = db.ReferenceField("Paste", required=True)

    created = db.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        if len(str(self.content)) > 50:
            return f"<Comment {self.author} - {str(self.content)[:50].strip()}..>"
        return f"<Comment {self.author} - {str(self.content)}>"


class Paste(db.Document):
    content = db.StringField(max_length=512000, required=True)

    category = db.StringField(choices=choices.CATEGORIES, required=False, default="None")
    tags = db.ListField(max_length=10, required=False)
    syntax = db.StringField(
        choices=choices.SYNTAXES,
        required=True,
        default="None",
    )
    paste_expiration = db.IntField(choices=choices.PASTE_EXPIRATION, required=True, default=0)
    paste_exposure = db.StringField(
        choices=choices.PASTE_EXPOSURE,
        required=True,
        default="Public",
    )
    paste_hash = db.StringField(default=lambda: str(uuid.uuid4())[:8], primary_key=True)
    title = db.StringField(max_length=50, required=False, default="Untitled")

    author = db.ReferenceField("User", required=True)
    comments = db.EmbeddedDocumentListField("Comment", required=False)

    created = db.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        if len(str(self.content)) > 50:
            return f"<Paste {self.author} - {str(self.content)[:50].strip()}..>"
        return f"<Paste {self.author} - {str(self.content)}>"
