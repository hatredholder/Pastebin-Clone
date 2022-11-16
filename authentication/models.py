from app import db

from flask_login import UserMixin


class User(UserMixin, db.Document):
    email = db.EmailField(max_length=100, unique=True, required=True)
    password_hash = db.StringField(max_length=1000, required=True)
    name = db.StringField(max_length=100, required=True)
