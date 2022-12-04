from flask import Blueprint, redirect, render_template, url_for

from flask_login import current_user, login_required

import pybin.forms as forms
import pybin.models as models
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

    if paste_hash:
        return redirect(url_for("pybin.paste_view", paste_hash=paste_hash))

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
@utils.is_author
def paste_delete(paste_hash):
    paste = utils.get_paste_from_hash(paste_hash)

    utils.delete_paste(paste)

    return redirect(url_for("pybin.home"))


@pybin.route("/edit/<paste_hash>/", methods=["GET", "POST"])
@login_required
@utils.paste_exists
@utils.is_author
def paste_edit(paste_hash):
    paste = utils.get_paste_from_hash(paste_hash)

    form = forms.PasteForm(obj=paste)

    if utils.edit_paste(form, paste):
        return redirect(url_for("pybin.paste_view", paste_hash=paste_hash))

    return render_template("pybin/edit_paste.html", form=form, paste=paste)


@pybin.route("/u/<username>/")
def my_pybin(username):
    user = utils.get_user_from_username(username)

    if not user:
        return redirect(url_for("pybin.error", error_code=404))

    pastes = models.Paste.objects(author=user)

    return render_template("pybin/my_pybin.html", pastes=reversed(pastes))


@pybin.route("/user/profile/", methods=["GET", "POST"])
@login_required
def profile():
    form = forms.ProfileForm()

    return render_template("pybin/profile.html", form=form)
