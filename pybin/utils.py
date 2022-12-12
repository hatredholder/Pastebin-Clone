import base64
import datetime
import functools
import io
import re

import authentication.models as auth_models

from flask import flash, redirect, url_for

from flask_login import current_user

import pybin.models as models

from wtforms.fields import StringField


# Helper Functions


def create_paste_if_submitted(form):
    """Returns paste hash if it gets created successfully"""

    if form.validate_on_submit():
        content = form.content.data
        category = form.category.data
        tags = form.tags.data
        syntax = form.syntax.data
        paste_expiration = form.paste_expiration.data
        paste_exposure = form.paste_exposure.data
        title = check_paste_title(form.title.data)

        # Returns None if > 10 tags
        if len(tags) > 10:
            flash("Max amount of tags is 10")
            return

        # Add paste
        paste = models.Paste(
            content=content,
            category=category,
            tags=tags,
            syntax=syntax,
            paste_expiration=paste_expiration,
            paste_exposure=paste_exposure,
            title=title,
            author=current_user,
        ).save()

        return paste.paste_hash


def get_paste_from_hash(paste_hash):
    """Returns paste from paste_hash"""
    return models.Paste.objects(paste_hash=paste_hash).first()


def get_user_from_username(username):
    """Returns user from username"""
    return auth_models.User.objects(username=username).first()


def delete_paste(paste):
    """Deletes paste and adds a flash message"""
    flash("Paste deleted successfully!")
    paste.delete()


def edit_paste(form, paste):
    """Return True if paste is edited successfully"""

    if form.validate_on_submit():
        content = form.content.data
        category = form.category.data
        tags = form.tags.data
        syntax = form.syntax.data
        paste_expiration = form.paste_expiration.data
        paste_exposure = form.paste_exposure.data
        title = check_paste_title(form.title.data)

        # Returns None if > 10 tags
        if len(tags) > 10:
            flash("Max amount of tags is 10")
            return

        paste.update(
            content=content,
            category=category,
            tags=tags,
            syntax=syntax,
            paste_expiration=paste_expiration,
            paste_exposure=paste_exposure,
            title=title,
            author=current_user,
        )

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
        # then set email_status to False,
        # so that the user has to verify it
        if email != user.email:
            user.update(
                email=email,
                email_status=False,
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


def create_base64_img_data():
    """Returns image data in base64 to display in html"""
    data = f"""
        data:image/png;base64, {
            base64.b64encode(current_user.avatar.read()).decode('utf-8')
        }
    """
    return data


# Decorators


def paste_exists(f):
    """Redirects user to 404 error page if paste doesn't exist"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):

        paste = get_paste_from_hash(kwargs["paste_hash"])

        if not paste:
            return redirect(url_for("pybin.error", error_code=404))

        result = f(*args, **kwargs)

        return result

    return wrapped


def paste_not_expired(f):
    """Deletes paste and redirects to 404 error page if paste is expired"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):

        paste = get_paste_from_hash(kwargs["paste_hash"])

        if (
            paste.paste_expiration > 0
            and datetime.datetime.now()
            > paste.created
            + datetime.timedelta(
                seconds=paste.paste_expiration,
            )
        ):
            paste.delete()
            return redirect(url_for("pybin.error", error_code=404))

        result = f(*args, **kwargs)

        return result

    return wrapped


def paste_exposed(f):
    """Redirects to 403 error page if paste is private and current_user != author"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):

        paste = get_paste_from_hash(kwargs["paste_hash"])

        if paste.paste_exposure == "Private" and paste.author != current_user:
            return redirect(url_for("pybin.error", error_code=403))

        result = f(*args, **kwargs)

        return result

    return wrapped


def is_author(f):
    """Redirects to 403 error page if current_user != author"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):

        paste = get_paste_from_hash(kwargs["paste_hash"])

        if paste.author != current_user:
            return redirect(url_for("pybin.error", error_code=403))

        result = f(*args, **kwargs)

        return result

    return wrapped


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
