import datetime

from app import db

from flask_login import UserMixin

import pybin.models as pybin_models


class User(UserMixin, db.Document):
    username = db.StringField(min_length=4, max_length=20, unique=True, required=True)
    email = db.EmailField(max_length=100, unique=True, required=True)

    email_verified = db.BooleanField(required=False, default=False)

    website_url = db.URLField(max_length=100, required=False)
    location = db.StringField(max_length=150, required=False)
    avatar = db.ImageField(
        size=(150, 150, True),
        required=False,
    )

    # Unset when user is registered through social authentication (Google, etc.)
    password_hash = db.StringField(max_length=1000, required=False)

    created = db.DateTimeField(default=datetime.datetime.now)

    # Setup avatar image when not set
    def clean(self):
        if not self.avatar:
            self.avatar.put(open("static/img/guest.png", "rb"))  # noqa: SIM115

    # Used in my_pybin.html template
    def get_total_rating(self):
        """Returns total rating from all pastes and comments the user made"""

        result = 0
        for i in pybin_models.Paste.objects(author=self):
            result += i.rating
        for i in pybin_models.Comment.objects(author=self):
            result += i.rating
        return result

    def __str__(self):
        return f"<User {self.username}>"
