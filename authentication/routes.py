import authentication.forms as forms
import authentication.models as models

from flask import Blueprint, flash, redirect, render_template, url_for

from flask_login import login_required, login_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = models.User.objects(username=username).first()

        # Check if user actually exists and check the password
        if not user or not check_password_hash(user.password_hash, password):
            flash("Please check your login details and try again.")
            return redirect(url_for("auth.login"))

        login_user(user)
        return redirect(url_for("pastebin.home"))

    return render_template("authentication/login.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = forms.SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = models.User.objects(email=email).first()

        # If email registered already - redirect back to signup
        if user:
            flash("Email address already exists.")
            return redirect(url_for("auth.signup"))

        # Add user
        new_user = models.User(
            email=email,
            username=username,
            password_hash=generate_password_hash(password),
        ).save()

        flash("Account created successfully!")
        login_user(new_user)
        return redirect(url_for("pastebin.home"))

    return render_template("authentication/signup.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("pastebin.home"))
