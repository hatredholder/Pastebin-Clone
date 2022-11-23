from flask_wtf import FlaskForm

from pastebin.utils import TagListField

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
        choices=[
            "None",
            "Cryptocurrency",
            "Cybersecurity",
            "Fixit",
            "Food",
            "Gaming",
            "Haiku",
            "Help",
            "History",
            "Housing",
            "Jokes",
            "Legal",
            "Money",
            "Movies",
            "Music",
            "Pets",
            "Photo",
            "Science",
            "Software",
            "Source Code",
            "Spirit",
            "Sports",
            "Travel",
            "TV",
            "Writing",
        ],
    )
    tags = TagListField(
        "Tags (separated by comma): ",
        separator=",",
    )
    paste_expiration = wtforms.SelectField(
        "Paste Expiration: ",
        choices=[
            (0, "Never"),
            (3600, "1 Hour"),
            (86400, "1 Day"),
            (2592000, "1 Month"),
            (31104000, "1 Year"),
        ],
    )
    paste_exposure = wtforms.SelectField(
        "Paste Exposure: ",
        choices=[
            "Public",
            "Unlisted",
            "Private",
        ],
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
