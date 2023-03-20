import functools
import io
import os
import pathlib
import random

from app import app, mail

import authentication.models as models

from captcha.image import ImageCaptcha

from flask import flash, redirect, request, send_file, session, url_for

from flask_login import current_user, login_user

from flask_mail import Message

from itsdangerous import BadSignature, URLSafeSerializer

import pybin.models as pybin_models

import requests

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


def create_email_verification_message(token, email, username):
    """Sends a email verification message to the specified email"""

    msg = Message(
        "Account registration at Pybin",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email],
    )

    link = url_for("auth.verify_email", token=token, _external=True)

    msg.body = f"Hello {username},\nFollow the link below to verify your email\n{link}"

    mail.send(msg)


def create_user_with_email_verification(email, username, password):
    """Creates a user and sends an email for verification"""

    # Add user
    new_user = models.User(
        email=email,
        username=username,
        password_hash=generate_password_hash(password),
    ).save()

    # Send a "My Messages" welcoming message
    create_welcoming_message(new_user)

    # Create token for email verification
    token = generate_token(email)

    # Send email verification message
    create_email_verification_message(token, email, new_user.username)

    flash(
        f"Hi {new_user.username}, \
          your account has been created! We have sent you an email to {new_user.email} with \
          an activation link in it. Please click on the activation link \
          to activate your account. ",
    )


def create_user_without_email_verification(email, username, password):
    """Creates a user without sending an email for verification"""

    new_user = models.User(
        email=email,
        username=username,
        password_hash=generate_password_hash(password),
        email_status=True,
    ).save()

    # Send a "My Messages" welcoming message
    create_welcoming_message(new_user)

    # Login the user
    login_user(new_user)


def signup_user_if_submitted(form):
    """Returns True if user was created successfully"""

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        captcha = form.captcha.data

        # If captcha incorrect - redirect back to signup
        if not check_if_captcha_correct(captcha):
            flash("The verification code is incorrect.")
            return

        # If email registered already - redirect back to signup
        if check_if_email_already_used(email):
            flash("Email address already exists.")
            return

        # If email verification is enabled
        if app.config.get("EMAIL_VERIFICATION_ENABLED", False):
            create_user_with_email_verification(email, username, password)
        else:
            create_user_without_email_verification(email, username, password)

        return True


def signup_user_from_social_media(form, email):
    """Returns True if user was created successfully"""

    if form.validate_on_submit():
        username = form.username.data

        new_user = models.User(
            email=email,
            username=username,
            email_status=True,
        ).save()

        # Send a "My Messages" welcoming message
        create_welcoming_message(new_user)

        # Delete session variables so user cant access
        # signup_from_social_media without authorizing through Google Again
        session.pop("google_auth")
        session.pop("email")

        login_user(new_user)

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

    # If email verification is enabled
    if app.config.get("EMAIL_VERIFICATION_ENABLED", False):
        if form.validate_on_submit():
            captcha = form.captcha.data
            user = current_user

            # If captcha incorrect - redirect back to signup
            if not check_if_captcha_correct(captcha):
                flash("The verification code is incorrect.")
                return

            # If current_user is not already logged in
            if not current_user.is_authenticated:
                user = models.User.objects(username=form.username.data).first()

            # If user is found
            if user:
                # If user email already verified
                if user.email_status:
                    flash("This username is not require verification.")
                    return

                # Create token for email verification
                token = generate_token(user.email)

                # Send email verification message
                create_email_verification_message(token, user.email, user.username)

                flash(
                    "We have sent you an email! \
                    It can sometimes take a few minutes before the email arrives. \
                    If you cannot find this email, please check your spam/junk inbox, \
                    sometimes the emails end up there. If you still cannot find the email, \
                    please contact us. ",
                )

            # If user is not found
            flash("This username is currently not registered in our database.")

    # If email verification is disabled
    else:
        flash("Email Verification is disabled!")


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


def create_flow_from_client_secrets_file():
    """Creates flow object from the client_secrets file"""
    from google_auth_oauthlib.flow import Flow

    # Find the client_secret file
    client_secrets_file = os.path.join(
        pathlib.Path(__file__).parent.parent, "client_secret.json",
    )

    # Create flow from client_secret file
    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
        ],
        redirect_uri="http://127.0.0.1:5000/login/callback",
    )

    return flow


def get_id_info_from_flow():
    """Returns info from the flow's response (user's gmail address, name, etc.)"""
    import google.auth.transport.requests
    from google.oauth2 import id_token
    from pip._vendor import cachecontrol

    # Create the flow
    flow = create_flow_from_client_secrets_file()

    # Fetch the token
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    # Grab the info
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=app.config["GOOGLE_CLIENT_ID"],
    )

    return id_info


def check_if_user_already_exists(email):
    """Returns True and logins user if user with specified email exists already"""

    user = models.User.objects(email=email).first()

    if user:
        login_user(user)
        return True


def check_if_social_authentication_is_enabled():
    """
    Returns False and sends a flash message
    if SOCIAL_AUTHENTICATION_ENABLED enviroment variable is set to False
    """

    if not app.config.get("SOCIAL_AUTHENTICATION_ENABLED", False):
        flash("Social authentication is disabled!")
        return False

    return True


def generate_captcha_code():
    """Generates a captcha verification code and puts it into session"""

    symbols = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
        "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    ]
    result = []

    # Take 6 and put them into result
    for _ in range(0, 6):
        result.append(random.choice(symbols))

    # Turn list into a string
    captcha = "".join(result)

    # Put inside a session variable
    session["captcha"] = captcha

    return captcha


def get_captcha_image():
    """Returns a PIL image of captcha"""

    image = ImageCaptcha()
    captcha_code = session.get("captcha")

    if not captcha_code:
        captcha_code = generate_captcha_code()

    captcha_image = image.generate_image(session.get("captcha", captcha_code))
    return captcha_image


def check_if_captcha_correct(captcha):
    """Returns True if captcha is correct"""
    
    if captcha.lower() == session["captcha"].lower():

        # Update captcha session variable
        generate_captcha_code()
        return True


def serve_pil_image(captcha):
    """Accepts and serves a PIL image"""

    image_buffer = io.BytesIO()
    captcha.save(image_buffer, "png")
    image_buffer.seek(0)  # return the read cursor to the start of the file

    return send_file(image_buffer, mimetype="image/jpeg")


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


def google_authorized(f):
    """Redirects to auth.signup if google_auth isn't set in session"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get("google_auth"):
            return redirect(url_for("auth.signup"))

        result = f(*args, **kwargs)

        return result

    return wrapped
