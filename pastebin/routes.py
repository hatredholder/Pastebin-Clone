from flask import Blueprint, flash, redirect, render_template, url_for

from flask_login import current_user, login_required

import pastebin.forms as forms
import pastebin.models as models
import pastebin.utils as utils


pastebin = Blueprint("pastebin", __name__)


@pastebin.route("/", methods=["GET", "POST"])
@login_required
def home():
    form = forms.PasteForm()

    if form.validate_on_submit():
        content = form.content.data
        category = form.category.data
        tags = form.tags.data
        paste_expiration = form.paste_expiration.data
        paste_exposure = form.paste_exposure.data
        title = utils.check_paste_title(form.title.data)

        # Redirect back to form if user submitted more than 10 tags
        if len(tags) > 10:
            flash("Max count of tags is 10")
            return redirect(url_for("pastebin.home"))

        # Add paste
        paste = models.Paste(
            content=content,
            category=category,
            tags=tags,
            paste_expiration=paste_expiration,
            paste_exposure=paste_exposure,
            title=title,
            author=current_user,
        ).save()

        return redirect(url_for("pastebin.paste_view", paste_hash=paste.paste_hash))

    return render_template("pastebin/home.html", form=form, name=current_user.username)


@pastebin.route("/not_found")
def not_found():
    return "Not Found (#404)"


@pastebin.route("/<paste_hash>")
def paste_view(paste_hash):
    paste = models.Paste.objects(paste_hash=paste_hash).first()

    if not utils.check_if_paste_exists(paste):
        return redirect(url_for("pastebin.not_found"))

    if utils.check_paste_expiration(paste):
        return redirect(url_for("pastebin.not_found"))

    return render_template("pastebin/paste.html", paste=paste)


@pastebin.route("/raw/<paste_hash>")
def paste_raw_view(paste_hash):
    paste = models.Paste.objects(paste_hash=paste_hash).first()

    if not utils.check_if_paste_exists(paste):
        return redirect(url_for("pastebin.not_found"))

    if utils.check_paste_expiration(paste):
        return redirect(url_for("pastebin.not_found"))

    return f"<pre>{paste.content}</pre>"


@pastebin.route("/delete/<paste_hash>")
@login_required
def paste_delete(paste_hash):
    paste = models.Paste.objects(paste_hash=paste_hash).first()

    if paste.author != current_user:
        flash("You can't delete this paste")
        return redirect(url_for("pastebin.paste_view", paste_hash=paste.paste_hash))

    flash("Paste deleted successfully!")
    paste.delete()

    return redirect(url_for("pastebin.home"))
