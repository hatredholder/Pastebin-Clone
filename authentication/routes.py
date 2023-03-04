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


@auth.route("/resend/", methods=["GET", "POST"])
def resend():
    form = forms.ResendForm()

    utils.resend_verification_email(form)

    return render_template("authentication/resend.html", form=form)


@auth.route("/verify-email/<token>/", methods=["GET", "POST"])
def verify_email(token):

    if utils.check_if_current_user_email_already_verified():
        return redirect(url_for("pybin.home"))

    email = utils.confirm_token(token)

    if utils.verify_user_email(email):
        return redirect(url_for("pybin.profile"))

    return redirect(url_for("pybin.error", error=400))
