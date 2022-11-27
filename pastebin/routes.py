from flask import Blueprint, redirect, render_template, request, url_for

from flask_login import current_user, login_required

import pastebin.forms as forms
import pastebin.utils as utils


pastebin = Blueprint("pastebin", __name__)


@pastebin.route("/error/<error_code>")
def error(error_code):
    return render_template("pastebin/error.html", error_code=error_code)


@pastebin.route("/", methods=["GET", "POST"])
@login_required
def home():
    form = forms.PasteForm()

    paste_hash = utils.create_paste_if_submitted(form)

    if request.method == "POST":

        if paste_hash:
            return redirect(url_for("pastebin.paste_view", paste_hash=paste_hash))

        return redirect(url_for("pastebin.home"))

    return render_template("pastebin/home.html", form=form, name=current_user.username)


@pastebin.route("/<paste_hash>")
@utils.paste_exists
@utils.paste_not_expired
@utils.paste_exposed
def paste_view(paste_hash):
    paste = utils.get_paste_from_hash(paste_hash)

    return render_template("pastebin/paste.html", paste=paste)


@pastebin.route("/raw/<paste_hash>")
@utils.paste_exists
@utils.paste_not_expired
@utils.paste_exposed
def paste_raw_view(paste_hash):
    paste = utils.get_paste_from_hash(paste_hash)

    return f"<pre>{paste.content}</pre>"


@pastebin.route("/delete/<paste_hash>")
@login_required
@utils.paste_exists
def paste_delete(paste_hash):
    paste = utils.get_paste_from_hash(paste_hash)

    if not utils.delete_paste_if_user_is_author(paste):
        return redirect(url_for("pastebin.paste_view", paste_hash=paste.paste_hash))

    return redirect(url_for("pastebin.home"))
