import functools

from app import app, mail

import authentication.models as models

from flask import flash, redirect, url_for

from flask_login import current_user, login_user

from flask_mail import Message

from itsdangerous import BadSignature, URLSafeSerializer

import pybin.models as pybin_models

from werkzeug.security import check_password_hash, generate_password_hash


# Helper Functions


def check_if_email_already_used(email):
    """Returns True if a user with specified email already exists"""
    user = models.User.objects(email=email).first()

    if user:
        flash("Email address already exists.")
        return True

    return False


def get_admin_user():
    """Returns Admin User object"""

    # If Admin User already exists - return it
    admin = models.User.objects(username="Admin").first()
    if admin:
        return admin

    # If it doesnt exist - create it and then return it
    admin = models.User(username="Admin", email="admin@email.com", password_hash="123")
    admin.save()
    return admin


def create_welcoming_message(new_user):
    """Creates a Message object with new_user as receiver and Admin as author"""

    username = new_user.username

    welcome = f"""Hello {username},

    Good to see that you have decided to join our community!

    We like to remind you that our website is mobile friendly, so you can create, \
    edit and delete pastes on your phone or tablet too.

    You can follow us on Facebook and Twitter.

    Kind regards,

    The Pybin Team"""

    pybin_models.Message(
        content=welcome,
        title="Welcome to Pybin!",
        author=get_admin_user(),
        receiver=new_user,
    ).save()


def create_email_confirmation_message(token, email, username):
    """Sends a email confirmation message to the specified email"""

    msg = Message(
        "Account registration at Pybin",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email],
    )

    link = url_for("auth.verify_email", token=token, _external=True)

    msg.body = f"Hello {username},\nFollow the link below to verify your email\n{link}"

    mail.send(msg)


def signup_user_if_submitted(form):
    """Returns True if user was created successfully"""

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # If email registered already - redirect back to signup
        if check_if_email_already_used(email):
            flash("Email address already exists.")
            return

        # Add user
        new_user = models.User(
            email=email,
            username=username,
            password_hash=generate_password_hash(password),
        ).save()

        # Send a "My Messages" welcoming message
        create_welcoming_message(new_user)

        # Create token for email confirmation
        token = generate_token(email)

        # Send email confirmation message
        create_email_confirmation_message(token, email, new_user.username)

        flash(
            f"Hi {new_user.username}, \
              your account has been created! We have sent you an email to {new_user.email} with \
              an activation link in it. Please click on the activation link \
              to activate your account. ",
        )

        return True


def login_user_if_submitted(form):
    """Returns True and logins user if submitted user credentials are correct"""

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = models.User.objects(username=username).first()

        # Check if user actually exists and check the password
        if not user or not check_password_hash(user.password_hash, password):
            flash("Please check your login details and try again.")
            return

        # Check if user email if verified
        if not user.email_status:
            flash(
                f"This account is not activated yet. \
                Please click the activation link first. \
                If you cannot find that link, \
                <a href=\"{url_for('auth.resend')}\"> request new activation email </a> \
                to resolve this!",
            )
            return

        login_user(user)
        return True


def check_if_current_user_email_already_verified():
    """Returns True if user is authenticated and email_status == True"""

    if current_user.is_authenticated and current_user.email_status:
        flash("Your email already verified.")

        return True


def verify_user_email(email):
    """Returns True if Email != False"""

    if email:
        user = models.User.objects(email=email).first()

        user.email_status = True
        user.save()

        login_user(user)
        flash("Your email has been confirmed!")

        return True


def resend_verification_email(form):
    """Sends a verification email if user with given username is found"""

    if form.validate_on_submit():

        user = current_user

        # If current_user is not already logged in
        if not current_user.is_authenticated:
            user = models.User.objects(username=form.username.data).first()

        # If user is found
        if user:

            # If user email already verified
            if user.email_status:
                flash("This username is not require verification.")
                return

            # Create token for email confirmation
            token = generate_token(user.email)

            # Send email confirmation message
            create_email_confirmation_message(token, user.email, user.username)

            flash(
                "We have sent you an email! \
                It can sometimes take a few minutes before the email arrives. \
                If you cannot find this email, please check your spam/junk inbox, \
                sometimes the emails end up there. If you still cannot find the email, \
                please contact us. ",
            )

        # If user is not found
        flash("This username is currently not registered in our database.")


def generate_token(email):
    serializer = URLSafeSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email)


def confirm_token(token):
    """Returns email if token is de-serialized successfully, False otherwise"""

    serializer = URLSafeSerializer(app.config["SECRET_KEY"])

    try:
        # Tries to get email from token, returns BadSignature if unsuccessful
        email = serializer.loads(
            token,
        )

        # If email is already verified - return false
        if models.User.objects(email=email).first().email_status:
            return False

        # Otherwise - return the de-serialized email
        return email

    # If invalid token - return False
    except BadSignature:
        return False


# Decorators


def not_authenticated(f):
    """Redirects to pybin.home if current_user is logged in"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):

        if current_user.is_authenticated:
            return redirect(url_for("pybin.home"))

        result = f(*args, **kwargs)

        return result

    return wrapped
