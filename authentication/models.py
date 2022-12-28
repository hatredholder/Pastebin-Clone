from app import db

from flask_login import UserMixin


class User(UserMixin, db.Document):
    username = db.StringField(min_length=4, max_length=20, unique=True, required=True)
    email = db.EmailField(max_length=100, unique=True, required=True)

    # Set to True by default until Email Verification is implemented
    # TODO: Implement Email Verification
    email_status = db.BooleanField(required=False, default=True)

    website_url = db.URLField(max_length=100, required=False)
    location = db.StringField(max_length=150, required=False)
    avatar = db.ImageField(
        size=(150, 150, False),
        required=False,
    )

    # TODO: Implement Social Authentication (Set required to False)
    password_hash = db.StringField(max_length=1000, required=True)

    def __str__(self):
        return f"<User {self.username}>"

    def clean(self):
        if not self.avatar:
            self.avatar.put(open("static/img/guest.png", "rb"))  # noqa: SIM115
