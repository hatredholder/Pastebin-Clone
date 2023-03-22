import base64
import datetime
import functools
import io
import re

from app import app

import authentication.models as auth_models
from authentication.utils import check_if_captcha_correct

from flask import flash, redirect, request, url_for

from flask_login import current_user

from mongoengine.queryset.visitor import Q

import pybin.forms as forms
import pybin.models as models

import timeago

from werkzeug.security import check_password_hash, generate_password_hash

from wtforms.fields import StringField


# Helper Functions


def create_paste_if_submitted(form):
    """Returns paste.uuid_hash if Paste gets created successfully"""

    if form.validate_on_submit():
        content = form.content.data
        category = form.category.data
        tags = form.tags.data
        syntax = form.syntax.data
        expiration = form.expiration.data
        exposure = form.exposure.data
        title = check_paste_title(form.title.data)

        # Returns None if > 10 tags
        if len(tags) > 10:
            flash("Max amount of tags is 10")
            return

        # Add author field to paste if user is authenticated
        if current_user.is_authenticated:
            paste = models.Paste(
                author=current_user,  # adding author
                content=content,
                category=category,
                tags=tags,
                syntax=syntax,
                expiration=expiration,
                exposure=exposure,
                title=title,
            ).save()
        else:
            paste = models.Paste(
                content=content,
                category=category,
                tags=tags,
                syntax=syntax,
                expiration=expiration,
                exposure=exposure,
                title=title,
            ).save()

        return paste.uuid_hash


def create_comment_if_submitted(form, document):
    """Returns True if Comment gets created successfully"""

    # If document is a Paste
    if type(document) == models.Paste:
        # Set paste to document
        paste = document

    # Else - document is a Comment
    else:
        # Set paste to document's paste
        paste = document.paste

    if form.validate_on_submit():
        content = form.content.data
        syntax = form.syntax.data

        comment = models.Comment(
            content=content,
            syntax=syntax,
            author=current_user,
            paste=paste,
        ).save()

        document.comments.append(comment)
        document.save()

        return True


def create_reply_if_submitted(form, message):
    """Returns True if Reply gets created successfully"""

    if form.validate_on_submit():
        content = form.content.data

        reply = models.Reply(
            content=content,
            author=current_user,
        )

        message.replies.append(reply)
        message.save()

        return True


def get_paste_from_hash(uuid_hash):
    """Returns Paste from uuid_hash"""
    return models.Paste.objects(uuid_hash=uuid_hash).first()


def get_comment_from_hash(uuid_hash):
    """Returns Comment from uuid_hash"""
    return models.Comment.objects(uuid_hash=uuid_hash).first()


def get_document_from_hash(uuid_hash):
    """Returns document (Paste or Comment) from uuid_hash"""
    document = get_paste_from_hash(uuid_hash)

    if not document:
        document = get_comment_from_hash(uuid_hash)

    return document


def get_message_from_hash(uuid_hash):
    """Returns Message from uuid_hash"""
    return models.Message.objects(uuid_hash=uuid_hash).first()


def get_user_from_username(username):
    """Returns user from username"""
    return auth_models.User.objects(username=username).first()


def delete_document(document):
    """Deletes document and adds a flash message"""

    # If document is a Paste
    if type(document) == models.Paste:
        # Find paste's comments
        comments = models.Comment.objects(paste=document)

        # Set their paste to None
        comments.update(
            paste=None,
        )

        document.delete()
        flash("Paste deleted successfully!")

    # If document is a Comment
    else:
        document.update(
            content="Comment was deleted",
            active=False,
        )
        flash("Comment deleted successfully!")


def redirect_by_document_type(document):
    """
    Redirects user to my_pybin route if document is a Paste,
    redirects to my_comments route if document is a Comment
    """
    if type(document) == models.Paste:
        return redirect(url_for("pybin.my_pybin", username=document.author.username))
    else:
        return redirect(url_for("pybin.my_comments", username=document.author.username))


def get_edit_form_by_document_type(document):
    """
    Returns PasteForm if document is Paste,
    returns Commentform if document is a Comment
    """
    if type(document) == models.Paste:
        form = forms.PasteForm(obj=document)
    else:
        form = forms.CommentForm(obj=document)
    return form


def edit_document(form, document):
    """Return True if document is edited successfully"""

    # If document is a Paste
    if type(document) == models.Paste:
        if form.validate_on_submit():
            content = form.content.data
            category = form.category.data
            tags = form.tags.data
            syntax = form.syntax.data
            expiration = form.expiration.data
            exposure = form.exposure.data
            title = check_paste_title(form.title.data)

            if len(tags) > 10:
                flash("Max amount of tags is 10")
                return

            document.update(
                content=content,
                category=category,
                tags=tags,
                syntax=syntax,
                expiration=expiration,
                exposure=exposure,
                title=title,
                author=current_user,
            )

            return True

    # Else document is a Comment
    else:
        if form.validate_on_submit():
            content = form.content.data
            syntax = form.syntax.data

            document.update(
                content=content,
                syntax=syntax,
            )

            return True


def check_if_comment_older_than_5_minutes(document):
    """Returns True if document is a Comment and its older than 5 minutes"""

    if (
        type(document) == models.Comment
        and document.created
        + datetime.timedelta(
            minutes=5,
        )
        < datetime.datetime.now()
    ):
        return True


def check_paste_title(title):
    """Returns 'Untitled' if title wasn't provided"""
    return title if title else "Untitled"


def update_profile(form, user):
    """Returns True if User model is updated successfully"""

    if form.validate_on_submit():
        email = form.email.data
        website_url = form.website_url.data
        location = form.location.data

        # Check if email entered by the user isn't used by someone already
        if email != user.email:  # noqa: SIM102
            if auth_models.User.objects(email=email).first():
                flash("This email address has already been taken.")
                return

        # Regex pattern that checks if url starts with http:// or https://
        url_pattern = re.compile(
            r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]"
            r"+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]"
            r"+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))"
            r"[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})",
        )

        # Returns None if url doesnt match pattern
        if website_url and not url_pattern.search(website_url):
            flash("Please make sure your website starts with http:// or https://")
            return

        # If user updated email,
        # then set email_verified to False,
        # so that the user has to verify it
        if email != user.email:
            user.update(
                email=email,
                email_verified=False,
            )

        user.update(
            website_url=website_url,
            location=location,
        )

        flash("Your settings have been saved!")
        return True


def update_avatar(form, user):
    """Returns True if Avatar was updated successfully"""

    if form.validate_on_submit():
        avatar = form.avatar.data

        user.avatar.replace(io.BytesIO(avatar.read()))
        user.save()

        return True


def update_password(form, user):
    """Returns True if Password was updated successfully"""

    if form.validate_on_submit():
        password = form.password.data
        captcha = form.captcha.data

        # If captcha incorrect - redirect back to signup
        if not check_if_captcha_correct(captcha):
            flash("The verification code is incorrect.")
            return

        if current_user.password_hash:
            current_password = form.current_password.data

            if not check_password_hash(user.password_hash, current_password):
                flash(
                    "Your current password is not correct.\
                    Please enter your current password correctly!",
                )
                return

        user.update(
            password_hash=generate_password_hash(password),
        )

        flash("Your password has been updated!")
        return True


def create_base64_img_data(user):
    """Returns image data in base64 to display in html"""
    data = f"""
        data:image/png;base64, {
            base64.b64encode(user.avatar.read()).decode('utf-8')
        }
    """
    user.avatar.seek(0)  # return the read cursor to the start of the file

    return data


def get_my_pastes(current_user):
    """Returns last 8 pastes current_user made"""
    my_pastes = models.Paste.objects.filter(author=current_user)[:8].order_by(
        "-created",
    )
    return my_pastes


def get_public_pastes(current_user):
    """Returns 8 most recenet public pastes"""
    public_pastes = models.Paste.objects.filter(exposure="Public")[:8].order_by(
        "-created",
    )
    return public_pastes


def get_messages(current_user):
    """Returns all messages that current_user sent or received"""
    messages = models.Message.objects(Q(author=current_user) | Q(receiver=current_user))
    return messages


def delete_reply_by_uuid_hash(message, reply_hash):
    """Deletes reply by uuid hash (wow thats a useful comment)"""
    message.update(pull__replies__uuid_hash=reply_hash)


def get_document_and_rating_value_from_request():
    """Gets document id and rating from request, sends document found by id and rating"""
    return get_document_from_hash(request.form.get("data_key")), request.form.get(
        "data_rating",
    )


def add_rating_to_document(document, rating_value):
    """Checks document rating status by current_user and adds rating"""

    # check if user is trying to rate their own document
    if document.author != current_user:
        # if like button is pressed
        if rating_value == "1":
            # if user already liked
            if current_user in document.liked:
                document.liked.remove(current_user)
                document.rating -= 1

            # if user already disliked
            elif current_user in document.disliked:
                document.disliked.remove(current_user)
                document.liked.append(current_user)
                document.rating += 2

            # if user didnt set a rating yet
            else:
                document.liked.append(current_user)
                document.rating += 1

        # if dislike button is pressed
        if rating_value == "-1":
            # if user already liked
            if current_user in document.liked:
                document.disliked.append(current_user)
                document.liked.remove(current_user)
                document.rating -= 2

            # if user already disliked
            elif current_user in document.disliked:
                document.disliked.remove(current_user)
                document.rating += 1

            # if user didnt set a rating yet
            else:
                document.disliked.append(current_user)
                document.rating -= 1

    document.save()


def create_rating_json_response(document):
    """Returns JSON response based on if current_user is trying to rate their own document"""

    if document.author != current_user:
        return {
            "key": document.id,
            "rating": document.rating,
            "likes": len(document.liked),
            "dislikes": len(document.disliked),
            "success": True,
        }
    else:
        return {"success": False}


def find_matching_pastes_from_search_query():
    """
    Returns QuerySet of matching Pastes found if search_query wasn't empty,
    returns None otherwise
    """
    search_query = request.args.get("q")

    if not search_query:
        return

    matching_pastes = models.Paste.objects.filter(
        Q(title__icontains=search_query) | Q(content__icontains=search_query),
    ).order_by("-created")

    return matching_pastes


# Decorators


def document_exists(f):
    """Redirects user to 404 error page if Paste doesn't exist"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        paste = get_paste_from_hash(kwargs["uuid_hash"])

        if not paste:
            comment = get_comment_from_hash(kwargs["uuid_hash"])

            if not comment or not comment.active:
                return redirect(url_for("pybin.error", error_code=404))

        result = f(*args, **kwargs)

        return result

    return wrapped


def paste_not_expired(f):
    """Deletes paste and redirects to 404 error page if Paste is expired"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        paste = get_paste_from_hash(kwargs["uuid_hash"])

        # If current document is a paste
        if paste:  # noqa: SIM102
            # If expiration > 0 (set to expire)
            # and datetime.now() > paste creation date + expiration time
            if (
                paste.expiration > 0
                and datetime.datetime.now()
                > paste.created
                + datetime.timedelta(
                    seconds=paste.expiration,
                )
            ):
                paste.delete()
                return redirect(url_for("pybin.error", error_code=404))

        result = f(*args, **kwargs)

        return result

    return wrapped


def paste_exposed(f):
    """Redirects to 403 error page if Paste is private and current_user != author"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        paste = get_paste_from_hash(kwargs["uuid_hash"])

        # If current document is a paste
        if paste:  # noqa: SIM102
            if paste.exposure == "Private" and paste.author != current_user:
                return redirect(url_for("pybin.error", error_code=403))

        result = f(*args, **kwargs)

        return result

    return wrapped


def is_author(f):
    """Redirects to 403 error page if current_user != author"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        document = get_document_from_hash(kwargs["uuid_hash"])

        if document.author != current_user:
            return redirect(url_for("pybin.error", error_code=403))

        result = f(*args, **kwargs)

        return result

    return wrapped


def message_exists(f):
    """Redirects user to 404 error page if Message doesn't exist"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        message = get_message_from_hash(kwargs["uuid_hash"])

        if not message:
            return redirect(url_for("pybin.error", error_code=404))

        result = f(*args, **kwargs)

        return result

    return wrapped


# Template Filters


@app.template_filter()
def timesince(date):
    return timeago.format(date, datetime.datetime.now())


# Fields


class TagListField(StringField):
    """Stringfield for a list of separated tags"""

    def __init__(
        self,
        label="",
        validators=None,
        remove_duplicates=True,
        to_lowercase=True,
        separator=" ",
        **kwargs,
    ):
        """
        Construct a new field.
        :param label: The label of the field.
        :param validators: A sequence of validators to call when validate is called.
        :param remove_duplicates: Remove duplicates in a case insensitive manner.
        :param to_lowercase: Cast all values to lowercase.
        :param separator: The separator that splits the individual tags.
        """
        super(TagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates
        self.to_lowercase = to_lowercase
        self.separator = separator
        self.data = []

    def _value(self):
        if self.data:
            return ", ".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(self.separator)]
            if self.remove_duplicates:
                self.data = list(self._remove_duplicates(self.data))
            if self.to_lowercase:
                self.data = [x.lower() for x in self.data if x != ""]

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item
