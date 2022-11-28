from flask import Blueprint, redirect, render_template, request, url_for

from flask_login import current_user, login_required

import pybin.forms as forms
import pybin.utils as utils


pybin = Blueprint("pybin", __name__)


@pybin.route("/error/<error_code>/")
def error(error_code):
    return render_template("pybin/error.html", error_code=error_code)


@pybin.route("/", methods=["GET", "POST"])
@login_required
def home():
    form = forms.PasteForm()

    paste_hash = utils.create_paste_if_submitted(form)

    if request.method == "POST":

        if paste_hash:
            return redirect(url_for("pybin.paste_view", paste_hash=paste_hash))

        return redirect(url_for("pybin.home"))

    return render_template("pybin/home.html", form=form, name=current_user.username)


@pybin.route("/<paste_hash>/")
@utils.paste_exists
@utils.paste_not_expired
@utils.paste_exposed
def paste_view(paste_hash):
    paste = utils.get_paste_from_hash(paste_hash)

    return render_template("pybin/paste.html", paste=paste)


@pybin.route("/raw/<paste_hash>/")
@utils.paste_exists
@utils.paste_not_expired
@utils.paste_exposed
def paste_raw_view(paste_hash):
    paste = utils.get_paste_from_hash(paste_hash)

    return f"<pre>{paste.content}</pre>"


@pybin.route("/delete/<paste_hash>/")
@login_required
@utils.paste_exists
def paste_delete(paste_hash):
    paste = utils.get_paste_from_hash(paste_hash)

    if not utils.delete_paste_if_user_is_author(paste):
        return redirect(url_for("pybin.paste_view", paste_hash=paste.paste_hash))

    return redirect(url_for("pybin.home"))


@pybin.route("/u/<username>/")
def my_pybin():
    ...
