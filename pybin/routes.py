from flask import Blueprint, redirect, render_template, url_for

from flask_login import current_user, login_required

import pybin.forms as forms
import pybin.models as models
import pybin.utils as utils

pybin = Blueprint("pybin", __name__)


@pybin.route("/", methods=["GET", "POST"])
@login_required
def home():
    form = forms.PasteForm()

    uuid_hash = utils.create_paste_if_submitted(form)

    if uuid_hash:
        return redirect(url_for("pybin.document_view", uuid_hash=uuid_hash))

    return render_template("pybin/home.html", form=form, name=current_user.username)


@pybin.route("/error/<error_code>/")
def error(error_code):
    return render_template("pybin/error.html", error_code=error_code)


@pybin.route("/<uuid_hash>/", methods=["GET", "POST"])
@utils.document_exists
@utils.paste_not_expired
@utils.paste_exposed
def document_view(uuid_hash):
    document = utils.get_document_from_hash(uuid_hash)

    form = forms.CommentForm()

    if utils.create_comment_if_submitted(form, document):
        return redirect(url_for("pybin.document_view", uuid_hash=uuid_hash))

    return render_template("pybin/document.html", document=document, form=form)


@pybin.route("/raw/<uuid_hash>/")
@utils.document_exists
@utils.paste_not_expired
@utils.paste_exposed
def document_raw_view(uuid_hash):
    document = utils.get_document_from_hash(uuid_hash)

    return f"<pre>{document.content}</pre>"


@pybin.route("/delete/<uuid_hash>/")
@login_required
@utils.document_exists
@utils.is_author
def document_delete(uuid_hash):
    document = utils.get_document_from_hash(uuid_hash)

    utils.delete_document(document)

    return utils.redirect_by_document_type(document)


@pybin.route("/edit/<uuid_hash>/", methods=["GET", "POST"])
@login_required
@utils.document_exists
@utils.is_author
def paste_edit(uuid_hash):
    paste = utils.get_paste_from_hash(uuid_hash)

    form = forms.PasteForm(obj=paste)

    if utils.edit_paste(form, paste):
        return redirect(url_for("pybin.document_view", uuid_hash=uuid_hash))

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


@pybin.route("/user/password/", methods=["GET", "POST"])
@login_required
@utils.email_verified
def password():
    form = forms.PasswordForm()

    if utils.update_password(form, current_user):
        return redirect(url_for("pybin.password"))

    return render_template("pybin/password.html", form=form)


@pybin.route("/u/<username>/comments/")
@login_required
def my_comments(username):
    user = utils.get_user_from_username(username)

    if not user:
        return redirect(url_for("pybin.error", error_code=404))

    comments = models.Comment.objects(author=user, active=True)

    return render_template("pybin/my_comments.html", comments=reversed(comments))
