from flask_wtf import FlaskForm, RecaptchaField

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
    recaptcha = RecaptchaField()
    submit = wtforms.SubmitField("Create My Account")


class LoginForm(FlaskForm):
    username = wtforms.StringField(
        "Your Username",
        validators=[
            valids.InputRequired(),
        ],
    )
    password = wtforms.PasswordField(
        "Your Password",
        validators=[
            valids.InputRequired(),
        ],
    )
    submit = wtforms.SubmitField("Submit")
