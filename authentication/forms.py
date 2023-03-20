from flask_wtf import FlaskForm

import wtforms
import wtforms.validators as valids


class SignupForm(FlaskForm):
    username = wtforms.StringField(
        "Username: ",
        validators=[
            valids.InputRequired(),
            valids.Length(min=3, max=20),
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
        render_kw={'style': 'width: 100px'},
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
        ],
    )
    submit = wtforms.SubmitField("Create My Account")


class LoginForm(FlaskForm):
    username = wtforms.StringField(
        "Username: ",
        validators=[
            valids.InputRequired(),
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
        render_kw={'style': 'width: 100px'},
        validators=[
            valids.InputRequired(),
        ],
    )
    submit = wtforms.SubmitField(
        "Resend Activation Email",
    )
