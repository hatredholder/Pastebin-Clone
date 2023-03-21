import re

from flask_wtf import FlaskForm

import wtforms
import wtforms.validators as valids
from wtforms.validators import ValidationError


# Validators


def no_special_symbols(form, field):
    regex = re.compile("[@!#$%^&*()<>?/\\|}{~:]")

    if regex.search(field.data):
        raise ValidationError(
            message="Only the following chars are allowed in usernames: A-Z, 0-9, - and _.",
        )


# Forms


class SignupForm(FlaskForm):
    username = wtforms.StringField(
        "Username: ",
        validators=[
            valids.InputRequired(),
            valids.Length(min=3, max=20),
            no_special_symbols,
        ],
    )
    email = wtforms.EmailField(
        "Email Address: ",
        validators=[
            valids.InputRequired(),
        ],
    )
    password = wtforms.PasswordField(
        "Password: ",
        validators=[
            valids.InputRequired(),
            valids.Length(min=12, max=30),
        ],
    )
    captcha = wtforms.StringField(
        render_kw={"style": "width: 120px"},
        validators=[
            valids.InputRequired(),
        ],
    )
    submit = wtforms.SubmitField("Create My Account")


class GoogleSignupForm(FlaskForm):
    username = wtforms.StringField(
        "Username: ",
        validators=[
            valids.InputRequired(),
            valids.Length(min=3, max=20),
            no_special_symbols,
        ],
    )
    submit = wtforms.SubmitField("Create My Account")


class LoginForm(FlaskForm):
    username = wtforms.StringField(
        "Username: ",
        validators=[
            valids.InputRequired(),
            valids.Length(max=20),
        ],
    )
    password = wtforms.PasswordField(
        "Password: ",
        validators=[
            valids.InputRequired(),
        ],
    )
    submit = wtforms.SubmitField("Login")


class ResendForm(FlaskForm):
    username = wtforms.StringField(
        "Username",
    )
    captcha = wtforms.StringField(
        render_kw={"style": "width: 120px"},
        validators=[
            valids.InputRequired(),
        ],
    )
    submit = wtforms.SubmitField(
        "Resend Activation Email",
    )
