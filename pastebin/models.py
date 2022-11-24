import datetime
import uuid

from app import db


CATEGORIES = (
    "None",
    "Cryptocurrency",
    "Cybersecurity",
    "Fixit",
    "Food",
    "Gaming",
    "Haiku",
    "Help",
    "History",
    "Housing",
    "Jokes",
    "Legal",
    "Money",
    "Movies",
    "Music",
    "Pets",
    "Photo",
    "Science",
    "Software",
    "Source Code",
    "Spirit",
    "Sports",
    "Travel",
    "TV",
    "Writing",
)

PASTE_EXPIRATION = (
    (0, "Never"),
    (3600, "1 Hour"),
    (86400, "1 Day"),
    (2592000, "1 Month"),
    (31104000, "1 Year"),
)

PASTE_EXPOSURE = (
    "Public",
    "Unlisted",
    "Private",
)


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

    category = db.StringField(choices=CATEGORIES, required=False, default="None")
    tags = db.ListField(max_length=10, required=False)
    title = db.StringField(max_length=50, required=False, default="Untitled")
    paste_expiration = db.IntField(choices=PASTE_EXPIRATION, required=True, default=0)
    paste_exposure = db.StringField(
        choices=PASTE_EXPOSURE, required=True, default="Public",
    )
    paste_hash = db.StringField(default=lambda: str(uuid.uuid4())[:8], primary_key=True)

    author = db.ReferenceField("User", required=True, reverse_delete_rule=db.CASCADE)
    comments = db.EmbeddedDocumentListField("Comment", required=False)

    created = db.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        if len(str(self.content)) > 50:
            return f"<Paste {self.author} - {str(self.content)[:50].strip()}..>"
        return f"<Paste {self.author} - {str(self.content)}>"
