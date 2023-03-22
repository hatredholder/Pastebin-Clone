from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from flask_login import current_user, login_required

import pybin.forms as forms
import pybin.models as models
import pybin.utils as utils

pybin = Blueprint("pybin", __name__)


@pybin.route("/", methods=["GET", "POST"])
def home():
    form = forms.PasteForm()

    uuid_hash = utils.create_paste_if_submitted(form)

    if uuid_hash:
        return redirect(url_for("pybin.document_view", uuid_hash=uuid_hash))

    return render_template("pybin/home.html", form=form)


@pybin.route("/error/<error_code>/")
def error(error_code):
    return render_template("pybin/error.html", error_code=error_code)


@pybin.route("/rating/", methods=["POST"])
def rating():
    if request.method == "POST":
        document, rating_value = utils.get_document_and_rating_value_from_request()

        utils.add_rating_to_document(document, rating_value)

        return jsonify(utils.create_rating_json_response(document))


@pybin.route("/<uuid_hash>/", methods=["GET", "POST"])
@utils.document_exists
@utils.paste_not_expired
@utils.paste_exposed
def document_view(uuid_hash):
    document = utils.get_document_from_hash(uuid_hash)

    form = forms.CommentForm()

    if utils.create_comment_if_submitted(form, document):
        return redirect(request.headers.get("Referer"))

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
def document_edit(uuid_hash):
    document = utils.get_document_from_hash(uuid_hash)

    form = utils.get_edit_form_by_document_type(document)

    if utils.check_if_comment_older_than_5_minutes(document):
        return redirect(url_for("pybin.error", error_code=403))

    if utils.edit_document(form, document):
        return redirect(url_for("pybin.document_view", uuid_hash=uuid_hash))

    if type(document) == models.Paste:
        return render_template("pybin/edit_paste.html", form=form, document=document)
    else:
        return render_template("pybin/edit_comment.html", form=form, document=document)


@pybin.route("/clone/<uuid_hash>/", methods=["GET", "POST"])
@login_required
@utils.document_exists
def document_clone(uuid_hash):
    document = utils.get_document_from_hash(uuid_hash)

    form = forms.PasteForm(obj=document)

    return render_template("pybin/clone_document.html", form=form)


@pybin.route("/message/<uuid_hash>/", methods=["GET", "POST"])
@login_required
@utils.message_exists
def message_view(uuid_hash):
    message = utils.get_message_from_hash(uuid_hash)

    form = forms.MessageForm()

    if utils.create_reply_if_submitted(form, message):
        return redirect(request.headers.get("Referer"))

    return render_template("pybin/message.html", form=form, message=message)


@pybin.route("/message/compose/")
@login_required
def send_message():
    # NOTE:
    # This route doesn't actually serve any functionality
    # and is made just to make pybin look more like pastebin
    return render_template("pybin/send_message.html")


@pybin.route("/reply/delete/<message_hash>/<reply_hash>/")
@login_required
def reply_delete(message_hash, reply_hash):
    message = utils.get_message_from_hash(message_hash)

    utils.delete_reply_by_uuid_hash(message, reply_hash)

    return redirect(request.headers.get("Referer"))


@pybin.route("/u/<username>/")
def my_pybin(username):
    user = utils.get_user_from_username(username)

    if not user:
        return redirect(url_for("pybin.error", error_code=404))

    pastes = models.Paste.objects(author=user).order_by("-created")

    return render_template("pybin/my_pybin.html", user=user, pastes=pastes)


@pybin.route("/u/<username>/comments/")
@login_required
def my_comments(username):
    user = utils.get_user_from_username(username)

    if not user:
        return redirect(url_for("pybin.error", error_code=404))

    comments = models.Comment.objects(author=user, active=True)

    return render_template(
        "pybin/my_comments.html",
        user=user,
        comments=reversed(comments),
    )


@pybin.route("/messages/")
@login_required
def my_messages():
    messages = utils.get_messages(current_user)

    return render_template("pybin/my_messages.html", messages=reversed(messages))


@pybin.route("/user/profile/", methods=["GET", "POST"])
@login_required
def profile():
    form = forms.ProfileForm(obj=current_user)

    if utils.update_profile(form, current_user):
        return redirect(url_for("pybin.profile"))

    return render_template("pybin/edit_profile.html", form=form)


@pybin.route("/user/change-avatar/", methods=["GET", "POST"])
@login_required
def avatar():
    form = forms.AvatarForm(obj=current_user)

    if utils.update_avatar(form, current_user):
        return redirect(url_for("pybin.my_pybin", username=current_user.username))

    return render_template("pybin/avatar.html", form=form)


@pybin.route("/search/")
@login_required
def search_pastes():
    matching_pastes = utils.find_matching_pastes_from_search_query()
    return render_template("pybin/search_pastes.html", matching_pastes=matching_pastes)
