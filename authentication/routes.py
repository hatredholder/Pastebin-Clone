import authentication.forms as forms
import authentication.utils as utils

from flask import Blueprint, redirect, render_template, url_for

from flask_login import login_required, logout_user


auth = Blueprint("auth", __name__)


@auth.route("/signup/", methods=["GET", "POST"])
@utils.not_authenticated
def signup():
    form = forms.SignupForm()

    if utils.signup_user_if_submitted(form):
        return redirect(url_for("pybin.home"))

    return render_template("authentication/signup.html", form=form)


@auth.route("/login/", methods=["GET", "POST"])
@utils.not_authenticated
def login():
    form = forms.LoginForm()

    if utils.login_user_if_submitted(form):
        return redirect(url_for("pybin.home"))

    return render_template("authentication/login.html", form=form)


@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("pybin.home"))
