from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import login_required, login_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash

from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("authentication/login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = bool(request.form.get("remember"))

    user = User.objects(email=email).first()

    # Check if user actually exists and check the password
    if not user or not check_password_hash(user.password_hash, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for("pastebin.profile"))


@auth.route("/signup")
def signup():
    return render_template("authentication/signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    user = User.objects(email=email).first()

    # If email registered already - redirect back to signup
    if user:
        flash("Email address already exists.")
        return redirect(url_for("auth.signup"))

    # Add user
    User(email=email, name=name, password_hash=generate_password_hash(password)).save()

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("pastebin.index"))
