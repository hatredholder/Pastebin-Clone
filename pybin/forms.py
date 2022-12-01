from flask_wtf import FlaskForm

import pybin.models as models
from pybin.utils import TagListField

import wtforms
import wtforms.validators as valids


class PasteForm(FlaskForm):
    content = wtforms.TextAreaField(
        "New Paste",
        validators=[
            valids.InputRequired(),
            valids.Length(
                max=512000,
                message="You have exceeded the maximum size of 512 kilobytes per Paste",
            ),
        ],
    )
    category = wtforms.SelectField(
        "Category: ",
        choices=list(models.CATEGORIES),
    )
    tags = TagListField(
        "Tags (separated by comma): ",
        separator=",",
    )
    paste_expiration = wtforms.SelectField(
        "Paste Expiration: ",
        choices=list(models.PASTE_EXPIRATION),
    )
    paste_exposure = wtforms.SelectField(
        "Paste Exposure: ",
        choices=list(models.PASTE_EXPOSURE),
    )
    title = wtforms.StringField(
        "Paste Name / Title: ",
        validators=[
            valids.Length(
                max=50,
                message="Paste title can't be longer than 50 symbols",
            ),
        ],
    )
    submit = wtforms.SubmitField(
        "Create New Paste",
    )
