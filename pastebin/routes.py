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
            flash('Max count of tags is 10')
            return redirect(url_for("pastebin.home"))

        # Add paste
        models.Paste(
            content=content,
            category=category,
            tags=tags,
            paste_expiration=paste_expiration,
            paste_exposure=paste_exposure,
            title=title,
            author=current_user,
        ).save()

        flash("Paste created successfully")
        return redirect(url_for("pastebin.home"))

    return render_template("pastebin/profile.html", form=form, name=current_user.username)
