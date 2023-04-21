import re

from flask_wtf import FlaskForm

import wtforms
import wtforms.validators as valids
from wtforms.validators import ValidationError


# Validators


def no_special_symbols(form, field):
    """
    Raises a ValidationError if field contains special symbols
    (symbols in the regex variable)
    """
    regex = re.compile("[@!#$%^&*()<>?/\\|}{~:]")

    if regex.search(field.data):
        raise ValidationError(
            message="Only the following chars are allowed in usernames: A-Z, 0-9, - and _.",
        )


# Forms


class SignupForm(FlaskForm):
    """
    Form used in the authentication.signup route
    """

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
    """
    Form used in the authentication.signup_from_social_media route
    """

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
    """
    Form used in the authentication.login route
    """

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


class PasswordForm(FlaskForm):
    """
    Form used in the authentication.password route
    """

    current_password = wtforms.PasswordField(
        "Current Password: ",
    )
    password = wtforms.PasswordField(
        "New Password: ",
        validators=[
            valids.InputRequired(),
            valids.Length(min=12, max=30),
            valids.EqualTo("password_confirm", message="Passwords must match"),
        ],
    )
    password_confirm = wtforms.PasswordField(
        "New Password Again: ",
        validators=[
            valids.InputRequired(),
            valids.EqualTo("password_confirm", message="Passwords must match"),
        ],
    )
    captcha = wtforms.StringField(
        render_kw={"style": "width: 120px"},
        validators=[
            valids.InputRequired(),
        ],
    )
    submit = wtforms.SubmitField(
        "Change Password",
    )


class ResendForm(FlaskForm):
    """
    Form used in the authentication.resend route
    """

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
