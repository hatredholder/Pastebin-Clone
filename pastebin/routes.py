from flask import Blueprint, redirect, render_template, request, url_for

from flask_login import current_user, login_required

import pastebin.forms as forms
import pastebin.utils as utils


pastebin = Blueprint("pastebin", __name__)


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


@pastebin.route("/not_found")
def not_found():
    return "Not Found (#404)"


@pastebin.route("/<paste_hash>")
def paste_view(paste_hash):
    paste = utils.get_paste_from_hash(paste_hash)

    if not utils.check_if_paste_exists(paste):
        return redirect(url_for("pastebin.not_found"))

    if utils.check_paste_expiration(paste):
        return redirect(url_for("pastebin.not_found"))

    return render_template("pastebin/paste.html", paste=paste)


@pastebin.route("/raw/<paste_hash>")
def paste_raw_view(paste_hash):
    paste = utils.get_paste_from_hash(paste_hash)

    if not utils.check_if_paste_exists(paste):
        return redirect(url_for("pastebin.not_found"))

    if utils.check_paste_expiration(paste):
        return redirect(url_for("pastebin.not_found"))

    return f"<pre>{paste.content}</pre>"


@pastebin.route("/delete/<paste_hash>")
@login_required
def paste_delete(paste_hash):
    paste = utils.get_paste_from_hash(paste_hash)

    if not utils.delete_paste_if_user_is_author(paste):
        return redirect(url_for("pastebin.paste_view", paste_hash=paste.paste_hash))

    return redirect(url_for("pastebin.home"))
