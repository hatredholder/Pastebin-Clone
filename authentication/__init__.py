from flask import Blueprint, redirect, render_template, url_for


auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("index.html")


# @auth.route('/login', methods=['POST'])
# def login_post():
#     return render_template('index.html')


@auth.route("/signup")
def signup():
    return render_template("signup.html")


# @auth.route('/signup', methods=['POST'])
# def signup_post():
#     return render_template('signup.html')


@auth.route("/logout")
def logout():
    return redirect(url_for("main.index"))
