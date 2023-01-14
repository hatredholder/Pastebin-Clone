import functools

import authentication.models as models

from flask import flash, redirect, url_for

from flask_login import current_user, login_user

import pybin.models as pybin_models

from werkzeug.security import check_password_hash, generate_password_hash


# Helper Functions


def get_admin_user():
    """Returns Admin User object"""

    # If Admin User already exists - return it
    admin = models.User.objects(username="Admin").first()
    if admin:
        return admin

    # If it doesnt exist - create it and then return it
    admin = models.User(username="Admin", email="admin@email.com", password_hash="123")
    admin.save()
    return admin


def create_welcoming_message(new_user):
    """Creates a Message object with new_user as receiver and Admin as author"""

    username = new_user.username

    welcome = f"""Hello {username},

    Good to see that you have decided to join our community!

    We like to remind you that our website is mobile friendly, so you can create, \
    edit and delete pastes on your phone or tablet too.

    You can follow us on Facebook and Twitter.

    Kind regards,

    The Pybin Team"""

    pybin_models.Message(
        content=welcome,
        title="Welcome to Pybin!",
        author=get_admin_user(),
        receiver=new_user,
    ).save()


def signup_user_if_submitted(form):
    """Returns True if user was created successfully"""

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = models.User.objects(email=email).first()

        # If email registered already - redirect back to signup
        if user:
            flash("Email address already exists.")
            return

        # Add user
        new_user = models.User(
            email=email,
            username=username,
            password_hash=generate_password_hash(password),
        ).save()

        create_welcoming_message(new_user)

        login_user(new_user)
        flash("Account created successfully!")

        return True


def login_user_if_submitted(form):
    """Returns True and logins user if submitted user credentials are correct"""

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = models.User.objects(username=username).first()

        # Check if user actually exists and check the password
        if not user or not check_password_hash(user.password_hash, password):
            flash("Please check your login details and try again.")
            return

        login_user(user)
        return True


# Decorators


def not_authenticated(f):
    """Redirects to pybin.home if current_user is logged in"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):

        if current_user.is_authenticated:
            return redirect(url_for("pybin.home"))

        result = f(*args, **kwargs)

        return result

    return wrapped
