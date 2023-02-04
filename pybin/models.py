import datetime
import uuid

from app import db

import pybin.choices as choices


class Paste(db.Document):
    content = db.StringField(max_length=512000, required=True)
    author = db.ReferenceField("User", required=False)

    uuid_hash = db.StringField(default=lambda: str(uuid.uuid4())[:8], primary_key=True)
    size = db.FloatField(required=False)
    title = db.StringField(max_length=50, required=False, default="Untitled")
    syntax = db.StringField(
        choices=choices.SYNTAXES,
        required=True,
        default="plaintext",
    )
    category = db.StringField(
        choices=choices.CATEGORIES,
        required=False,
        default="None",
    )
    tags = db.ListField(max_length=10, required=False)
    expiration = db.IntField(
        choices=choices.EXPIRATION,
        required=True,
        default=0,
    )
    exposure = db.StringField(
        choices=choices.EXPOSURE,
        required=True,
        default="Public",
    )

    rating = db.IntField(required=False, default=0)
    liked = db.ListField(db.ReferenceField("User"))
    disliked = db.ListField(db.ReferenceField("User"))

    comments = db.ListField(db.ReferenceField("Comment"))

    created = db.DateTimeField(default=datetime.datetime.now)

    def clean(self):
        # Set size on document save
        self.size = float(str(len(self.content) / 1000)[:4])

    def __str__(self):
        if len(str(self.content)) > 50:
            return f"<Paste {self.author} - {str(self.content)[:50].strip()}..>"
        return f"<Paste {self.author} - {str(self.content)}>"


class Comment(db.Document):
    content = db.StringField(max_length=512000, required=True)
    author = db.ReferenceField("User", required=True)
    active = db.BooleanField(required=True, default=True)

    uuid_hash = db.StringField(default=lambda: str(uuid.uuid4())[:8], primary_key=True)
    syntax = db.StringField(
        choices=choices.SYNTAXES,
        required=True,
        default="None",
    )
    size = db.FloatField(required=False)
    paste = db.ReferenceField("Paste", required=False)

    rating = db.IntField(required=False, default=0)
    liked = db.ListField(db.ReferenceField("User"))
    disliked = db.ListField(db.ReferenceField("User"))

    comments = db.ListField(
        db.ReferenceField("self"),
    )  # referencing 'self' to create replies

    created = db.DateTimeField(default=datetime.datetime.now)

    def clean(self):
        # Set size on document save
        self.size = float(str(len(self.content) / 1000)[:4])

    def __str__(self):
        if len(str(self.content)) > 50:
            return f"<Comment {self.author} - {str(self.content)[:50].strip()}..>"
        return f"<Comment {self.author} - {str(self.content)}>"


class Reply(db.EmbeddedDocument):
    content = db.StringField(max_length=10000, required=True)
    author = db.ReferenceField("User", required=True)

    uuid_hash = db.StringField(default=lambda: str(uuid.uuid4())[:8], primary_key=True)

    created = db.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        if len(str(self.content)) > 50:
            return f"<Reply {self.author} - {str(self.content)[:50].strip()}..>"
        return f"<Reply {self.author} - {str(self.content)}>"


class Message(db.Document):
    content = db.StringField(max_length=10000, required=True)
    author = db.ReferenceField("User", required=True)
    receiver = db.ReferenceField("User", required=True)

    uuid_hash = db.StringField(default=lambda: str(uuid.uuid4())[:8], primary_key=True)
    title = db.StringField(max_length=50, required=False, default="Untitled")

    replies = db.ListField(
        db.EmbeddedDocumentField("Reply"),
    )

    created = db.DateTimeField(default=datetime.datetime.now)

    def get_last_reply_creation_date(self):
        """Returns last reply creation date"""

        if self.replies:
            return self.replies[-1].created
        return self.created

    def __str__(self):
        if len(str(self.content)) > 50:
            return f"<Message {self.author} - {str(self.content)[:50].strip()}..>"
        return f"<Message {self.author} - {str(self.content)}>"
