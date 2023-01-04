import authentication.models as models

from flask import flash

from flask_login import login_user

from werkzeug.security import check_password_hash, generate_password_hash


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

        flash("Account created successfully!")
        login_user(new_user)
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
