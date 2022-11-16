from flask import Blueprint, flash, redirect, render_template, request, url_for

from werkzeug.security import generate_password_hash

from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("authentication/login.html")


# @auth.route('/login', methods=['POST'])
# def login_post():
#     return render_template('index.html')


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
    User(email=email, name=name, password=generate_password_hash(password)).save()

    return redirect(url_for("auth.login"))


@auth.route("/logout")
def logout():
    return redirect(url_for("pastebin.index"))
