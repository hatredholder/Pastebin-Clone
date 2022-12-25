from flask import Blueprint, redirect, render_template, url_for

from flask_login import current_user, login_required

import pybin.forms as forms
import pybin.models as models
import pybin.utils as utils

pybin = Blueprint("pybin", __name__)


# Context Processors


@pybin.context_processor
def utility_processor():
    def profile_image():
        avatar = utils.create_base64_img_data()
        return avatar

    return dict(profile_image=profile_image)


@pybin.context_processor
def my_pastes():
    def __my_pastes():
        pastes = utils.get_my_pastes(current_user)
        return pastes

    return dict(my_pastes=__my_pastes)


@pybin.context_processor
def public_pastes():
    def __public_pastes():
        pastes = utils.get_my_pastes(current_user)
        return pastes

    return dict(my_pastes=__public_pastes)


# Routes


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
    form = forms.ProfileForm(obj=current_user)

    if utils.update_profile(form, current_user):
        return redirect(url_for("pybin.profile"))

    return render_template("pybin/profile.html", form=form)


@pybin.route("/user/change-avatar/", methods=["GET", "POST"])
@login_required
def avatar():
    form = forms.AvatarForm(obj=current_user)

    if utils.update_avatar(form, current_user):
        return redirect(url_for("pybin.my_pybin", username=current_user.username))

    return render_template("pybin/avatar.html", form=form)
