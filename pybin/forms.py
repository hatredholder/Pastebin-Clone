from flask_wtf import FlaskForm

import pybin.choices as choices
import pybin.utils as utils

import wtforms
import wtforms.validators as valids


class PasteForm(FlaskForm):
    """
    Form used in the pybin.home route and pybin.document_clone route
    """

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
        choices=list(choices.CATEGORIES),
    )
    tags = utils.TagListField(
        "Tags (separated by comma): ",
        separator=",",
    )
    syntax = wtforms.SelectField(
        "Syntax Highlighting: ",
        choices=list(choices.SYNTAXES),
    )
    expiration = wtforms.SelectField(
        "Paste Expiration: ",
        choices=list(choices.EXPIRATION),
    )
    exposure = wtforms.SelectField(
        "Paste Exposure: ",
        choices=list(choices.EXPOSURE),
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


class ProfileForm(FlaskForm):
    """
    Form used in the pybin.profile route
    """

    email = wtforms.EmailField(
        "Email Address: ",
        validators=[
            valids.InputRequired(),
        ],
    )
    website_url = wtforms.StringField(
        "Website URL: ",
        validators=[
            valids.Length(
                max=100,
                message="Website URL should contain at most 100 characters.",
            ),
        ],
    )
    location = wtforms.StringField(
        "Location: ",
        validators=[
            valids.Length(
                max=150,
                message="Location should contain at most 150 characters.",
            ),
        ],
    )
    submit = wtforms.SubmitField(
        "Update Profile",
    )


class AvatarForm(FlaskForm):
    """
    Form used in the pybin.avatar route
    """

    avatar = wtforms.FileField(
        "Avatar (jpg/png/gif): ",
    )
    submit = wtforms.SubmitField(
        "Upload Avatar",
    )


class CommentForm(FlaskForm):
    """
    Form used in the pybin.document_view route
    """

    content = wtforms.TextAreaField(
        "Your Comment",
        validators=[
            valids.InputRequired(),
            valids.Length(
                max=512000,
                message="You have exceeded the maximum size of 512 kilobytes per Comment",
            ),
        ],
    )
    syntax = wtforms.SelectField(
        "Syntax Highlighting: ",
        choices=list(choices.SYNTAXES),
    )
    submit = wtforms.SubmitField(
        "Add Comment",
    )


class MessageForm(FlaskForm):
    """
    Form used in the pybin.message_view route
    """

    content = wtforms.TextAreaField(
        validators=[
            valids.InputRequired(),
            valids.Length(
                max=10000,
                message="Message should contain at most 10,000 characters.",
            ),
        ],
    )
    submit = wtforms.SubmitField(
        "Add Reply",
    )
