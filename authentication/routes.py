import authentication.forms as forms
import authentication.models as models
import authentication.utils as utils

from flask import Blueprint, flash, redirect, render_template, url_for

from flask_login import current_user, login_required, login_user, logout_user


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

    return render_template("authentication/resend.html", form=form)


@auth.route("/verify-email/<token>/", methods=["GET", "POST"])
def verify_email(token):

    if current_user.email_status:
        flash("Your email already verified.")
        return redirect(url_for("pybin.home"))

    email = utils.confirm_token(token)

    if email:
        user = models.User.objects(email=email)

        user.email_status = True
        user.save()

        login_user(user)
        flash("Your email has been confirmed!")

        return redirect(url_for("pybin.profile"))

    return redirect(url_for("pybin.error", error=400))
