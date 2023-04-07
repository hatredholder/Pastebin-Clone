import authentication.forms as forms
import authentication.models as models
import authentication.utils as utils

import pytest

from werkzeug.security import check_password_hash


# Signup Route


def test_signup_route_template_and_context(client, captured_templates):
    """
    GIVEN a Flask client and captured_templates function
    WHEN the "/signup/" page is requested
    THEN check if template used is "authentication/signup.html" and
    form in context is of type SignupForm
    """
    response = client.get("/signup/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "authentication/signup.html"
    assert type(context.get("form")) == forms.SignupForm


def test_signup_route_signup_user(client):
    """
    GIVEN a Flask client
    WHEN a POST request with data is sent to "/signup/" page
    THEN check if user got created
    """
    # Access "/site/captcha" to generate a captcha code
    response = client.get("/site/captcha/")
    assert response.status_code == 200

    with client.session_transaction() as session:
        data = {
            "username": "new_signup_user",
            "email": "new_signup_user@gmail.com",
            "password": "new_signup_password",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    response = client.post("/signup/", data=data)
    assert response.status_code == 302

    # Check if admin user got created
    # (admin user sends the welcoming message to newly signed up users)
    assert utils.get_admin_user()

    assert models.User.objects.first().username == "new_signup_user"


def test_signup_route_signup_user_special_symbols(client):
    """
    GIVEN a Flask client
    WHEN a POST request with data is sent to "/signup/" page
    THEN check if user got created
    """
    # Access "/site/captcha" to generate a captcha code
    response = client.get("/site/captcha/")
    assert response.status_code == 200

    with client.session_transaction() as session:
        data = {
            "username": "new_signup_user@!#$%^&*",
            "email": "new_signup_user@gmail.com",
            "password": "new_signup_password",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    response = client.post("/signup/", data=data)
    assert response.status_code == 200

    assert (
        b"Only the following chars are allowed in usernames: A-Z, 0-9, - and _."
        in response.data
    )


def test_signup_route_signup_user_incorrect_captcha(client):
    """
    GIVEN a Flask client
    WHEN a POST request with incorrect captcha data is sent to "/signup/" page
    THEN check if user didn't get created and flash message is displayed
    """
    data = {
        "username": "new_signup_user",
        "email": "new_signup_user@gmail.com",
        "password": "new_signup_password",
        "captcha": "incorrect captcha",
        "submit": "",
    }

    response = client.post("/signup/", data=data)
    assert response.status_code == 200

    assert len(models.User.objects.all()) == 0
    assert b"The verification code is incorrect." in response.data


def test_signup_route_signup_user_already_used_username(client, create_test_user):
    """
    GIVEN a Flask client and a test user object
    WHEN a POST request with already used username data is sent to "/signup/" page
    THEN check if flash message is displayed
    """
    # Access "/site/captcha" to generate a captcha code
    response = client.get("/site/captcha/")
    assert response.status_code == 200

    with client.session_transaction() as session:
        data = {
            "username": "new_user",
            "email": "new_user@gmail.com",
            "password": "new_signup_password",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    response = client.post("/signup/", data=data)
    assert response.status_code == 200

    assert b"This username has already been taken." in response.data


def test_signup_route_signup_user_already_used_email(client, create_test_user):
    """
    GIVEN a Flask client and a test user object
    WHEN a POST request with already used email data is sent to "/signup/" page
    THEN check if flash message is displayed
    """
    # Access "/site/captcha" to generate a captcha code
    response = client.get("/site/captcha/")
    assert response.status_code == 200

    with client.session_transaction() as session:
        data = {
            "username": "new_signup_user",
            "email": "new_user@gmail.com",
            "password": "new_signup_password",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    response = client.post("/signup/", data=data)
    assert response.status_code == 200

    assert b"Email address already exists." in response.data


def test_signup_route_signup_user_email_verification_enabled(
    client,
    enable_email_verification,
):
    """
    GIVEN a Flask client and email verification enabled
    WHEN a POST request with data is sent to "/signup/" page
    THEN check if user got created and his email is unverified
    """
    # Access "/site/captcha" to generate a captcha code
    response = client.get("/site/captcha/")
    assert response.status_code == 200

    with client.session_transaction() as session:
        data = {
            "username": "new_signup_user",
            "email": "new_signup_user@gmail.com",
            "password": "new_signup_password",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    response = client.post("/signup/", data=data)
    assert response.status_code == 302

    assert models.User.objects.first().email_verified == False  # noqa: E712


def test_signup_route_signup_user_email_verification_mail_username_not_set(
    client,
    enable_email_verification,
    app,
):
    """
    GIVEN a Flask client, email verification enabled, and app
    WHEN a POST request with data is sent to "/signup/" page
    THEN check if ValueError is raised when MAIL_USERNAME is set to None/unset
    """
    # Access "/site/captcha" to generate a captcha code
    response = client.get("/site/captcha/")
    assert response.status_code == 200

    app.config["MAIL_USERNAME"] = ""

    with client.session_transaction() as session:
        data = {
            "username": "new_signup_user",
            "email": "new_signup_user@gmail.com",
            "password": "new_signup_password",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    with pytest.raises(ValueError):
        response = client.post("/signup/", data=data)


def test_signup_route_already_authenticated(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN the "/signup/" page is requested
    THEN check if user gets redirected
    """
    response = authorized_client.get("/signup/")
    assert response.status_code == 302


# Login Route


def test_login_route_template_and_context(client, captured_templates):
    """
    GIVEN a Flask client and captured_templates function
    WHEN the "/login/" page is requested
    THEN check if template used is "authentication/login.html" and
    form in context is of type LoginForm
    """
    response = client.get("/login/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "authentication/login.html"
    assert type(context.get("form")) == forms.LoginForm


def test_login_route_login_user(client, create_test_user):
    """
    GIVEN a Flask client and a test user object
    WHEN a POST request with login data of create_test_user is sent to "/login/" page
    THEN check if user got logged in
    """
    data = {
        "username": "new_user",
        "password": "new_user_password",
        "submit": "",
    }

    response = client.post("/login/", data=data)
    assert response.status_code == 302

    # If _user_id is present in session - user is logged in
    with client.session_transaction() as session:
        assert session.get("_user_id")


def test_login_route_login_user_incorrect_password(client, create_test_user):
    """
    GIVEN a Flask client and a test user object
    WHEN a POST request with incorrect password data of create_test_user is sent to "/login/" page
    THEN check if flash message is displayed
    """
    data = {
        "username": "new_user",
        "password": "new_user_incorrect_password",
        "submit": "",
    }

    response = client.post("/login/", data=data)
    assert response.status_code == 200

    assert b"Please check your login details and try again." in response.data


def test_login_route_login_user_email_unverified(client, create_test_user):
    """
    GIVEN a Flask client and a test user object
    WHEN a POST request with unverified email data of create_test_user is sent to "/login/" page
    THEN check if flash message is displayed
    """
    # Set email to unverified
    create_test_user.update(
        email_verified=False,
    )

    data = {
        "username": "new_user",
        "password": "new_user_password",
        "submit": "",
    }

    response = client.post("/login/", data=data)
    assert response.status_code == 200

    assert b"This account is not activated yet." in response.data


# Logout route


def test_logout_route(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN the "/logout/" page is requested
    THEN check if user is now unauthorized
    """
    response = authorized_client.get("/logout/")

    assert response.status_code == 302

    # If _user_id is not present in session - user is not logged in
    with authorized_client.session_transaction() as session:
        assert not session.get("_user_id")


def test_logout_route_redirect_unauthorized_user(client):
    """
    GIVEN a Flask client
    WHEN the "/logout/" page is requested
    THEN check if unauthorized user gets redirected
    """
    response = client.get("/logout/")
    assert response.status_code == 302


# Password route


def test_password_route_template_and_context(authorized_client, captured_templates):
    """
    GIVEN an authorized Flask client and captured_templates function
    WHEN the "/user/password/" page is requested
    THEN check if template used is "authentication/password.html" and
    form in context is of type SignupForm
    """
    response = authorized_client.get("/user/password/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "authentication/password.html"
    assert type(context.get("form")) == forms.PasswordForm


def test_password_route_update_password(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "/user/password/" page
    THEN check if password got updated
    """
    # Access "/site/captcha" to generate a captcha code
    response = authorized_client.get("/site/captcha/")
    assert response.status_code == 200

    with authorized_client.session_transaction() as session:
        data = {
            "current_password": "new_user_password",
            "password": "updated_password",
            "password_confirm": "updated_password",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    response = authorized_client.post("/user/password/", data=data)
    assert response.status_code == 302

    response = authorized_client.get("/user/password/")

    # Check if password has been updated
    assert check_password_hash(
        models.User.objects(username="new_user").first().password_hash,
        "updated_password",
    )


def test_password_route_incorrect_captcha(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with incorrect captcha data is sent to "/user/password/" page
    THEN check if flash message is displayed
    """
    data = {
        "current_password": "new_user_password",
        "password": "updated_password",
        "password_confirm": "updated_password",
        "captcha": "incorrect_captcha",
        "submit": "",
    }

    response = authorized_client.post("/user/password/", data=data)
    assert response.status_code == 200

    assert b"The verification code is incorrect." in response.data


def test_password_route_blank_current_password(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "/user/password/" page
    THEN check if flash message is displayed
    """
    # Access "/site/captcha" to generate a captcha code
    response = authorized_client.get("/site/captcha/")
    assert response.status_code == 200

    with authorized_client.session_transaction() as session:
        data = {
            "current_password": "",
            "password": "updated_password",
            "password_confirm": "updated_password",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    response = authorized_client.post("/user/password/", data=data)
    assert response.status_code == 200

    assert b"Current Password cannot be blank." in response.data


def test_password_route_incorrect_current_password(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "/user/password/" page
    THEN check if flash message is displayed
    """
    # Access "/site/captcha" to generate a captcha code
    response = authorized_client.get("/site/captcha/")
    assert response.status_code == 200

    with authorized_client.session_transaction() as session:
        data = {
            "current_password": "incorrect_current_password",
            "password": "updated_password",
            "password_confirm": "updated_password",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    response = authorized_client.post("/user/password/", data=data)
    assert response.status_code == 200

    assert b"Your current password is not correct." in response.data


def test_password_route_redirect_unauthorized_user(client):
    """
    GIVEN a Flask client
    WHEN the "/user/password/" page is requested
    THEN check if unauthorized user gets redirected
    """
    response = client.get("/user/password/")
    assert response.status_code == 302


def test_password_route_redirect_unverified_email_user(
    authorized_client,
    create_test_user,
):
    """
    GIVEN an authorized Flask client and test user object
    WHEN the "/user/password/" page is requested and test user's email is set to unverified
    THEN check if authorized user with unverified email gets redirected
    """
    # Set email to unverified
    create_test_user.update(
        email_verified=False,
    )

    response = authorized_client.get("/user/password/")
    assert response.status_code == 302


# Resend route


def test_resend_route_template_and_context(client, captured_templates):
    """
    GIVEN a Flask client and captured_templates function
    WHEN the "/resend/" page is requested
    THEN check if template used is "authentication/signup.html" and
    form in context is of type SignupForm
    """
    response = client.get("/resend/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "authentication/resend.html"
    assert type(context.get("form")) == forms.ResendForm


def test_resend_route_send_email(
    client,
    enable_email_verification,
    create_test_user,
):
    """
    GIVEN an authorized Flask client, enabled email verification and test user object
    WHEN a POST request with data is sent to "/resend/" page
    THEN check if flash message is displayed
    """
    # Access "/site/captcha" to generate a captcha code
    response = client.get("/site/captcha/")
    assert response.status_code == 200

    # Set email to unverified
    create_test_user.update(
        email_verified=False,
    )

    with client.session_transaction() as session:
        data = {
            "username": "new_user",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    response = client.post("/resend/", data=data)
    assert response.status_code == 200

    assert b"We have sent you an email!" in response.data


def test_resend_route_incorrect_captcha(
    client,
    enable_email_verification,
    create_test_user,
):
    """
    GIVEN an authorized Flask client, enabled email verification and test user object
    WHEN a POST request with incorrect captcha data is sent to "/resend/" page
    THEN check if flash message is displayed
    """
    data = {
        "username": "new_user",
        "captcha": "incorrect_captcha",
        "submit": "",
    }

    response = client.post("/resend/", data=data)
    assert response.status_code == 200

    assert b"The verification code is incorrect." in response.data


def test_resend_route_doesnt_require_verification(
    client,
    enable_email_verification,
    create_test_user,
):
    """
    GIVEN an authorized Flask client, enabled email verification and test user object
    WHEN a POST request with data is sent to "/resend/" page
    THEN check if flash message is displayed
    """
    # Access "/site/captcha" to generate a captcha code
    response = client.get("/site/captcha/")
    assert response.status_code == 200

    with client.session_transaction() as session:
        data = {
            "username": "new_user",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    response = client.post("/resend/", data=data)
    assert response.status_code == 200

    assert b"This username is not require verification." in response.data


def test_resend_route_user_not_registered(client, enable_email_verification):
    """
    GIVEN an authorized Flask client and enabled email verification
    WHEN a POST request with data is sent to "/resend/" page
    THEN check if flash message is displayed
    """
    # Access "/site/captcha" to generate a captcha code
    response = client.get("/site/captcha/")
    assert response.status_code == 200

    with client.session_transaction() as session:
        data = {
            "username": "new_user",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    response = client.post("/resend/", data=data)
    assert response.status_code == 200

    assert (
        b"This username is currently not registered in our database." in response.data
    )


def test_resend_route_email_verification_disabled(client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "/resend/" page
    THEN check if flash message is displayed
    """
    # Access "/site/captcha" to generate a captcha code
    response = client.get("/site/captcha/")
    assert response.status_code == 200

    with client.session_transaction() as session:
        data = {
            "username": "new_user",
            "captcha": session.get("captcha"),  # get generated captcha code
            "submit": "",
        }

    response = client.post("/resend/", data=data)
    assert response.status_code == 200

    assert b"Email Verification is disabled!" in response.data


# Verify_email route


def test_verify_email_route_verify_email(authorized_client, create_test_user):
    """
    GIVEN an authorized Flask client and test user object
    WHEN the "/verify-email/<token>/" page where "token" is correct is requested
    THEN check if client with unverified email gets their email verified
    """
    # Set email to unverified
    create_test_user.update(
        email_verified=False,
    )

    token = utils.generate_token(create_test_user.email)

    authorized_client.get(f"/verify-email/{token}/")

    assert create_test_user.email_verified == True  # noqa: E712


def test_verify_email_route_email_already_verified(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN the "/verify-email/" page is requested
    THEN check if client with already verified email gets redirected to home url
    """
    response = authorized_client.get("/verify-email/token/", follow_redirects=True)

    assert response.request.path == "/"


def test_verify_email_route_invalid_token(authorized_client, create_test_user):
    """
    GIVEN an authorized Flask client and test user object
    WHEN the "/verify-email/<token>/" page where "token" is incorrect is requested
    THEN check if client gets redirected to error url
    """
    # Set email to unverified
    create_test_user.update(
        email_verified=False,
    )

    response = authorized_client.get(
        "/verify-email/incorrect_token/",
        follow_redirects=True,
    )

    assert response.request.path == "/error/400/"


# Auth_google route


def test_auth_google(client, enable_social_authentication):
    """
    GIVEN a Flask client and enabled social authentication
    WHEN the "/site/auth-google" is requested
    THEN check if client gets redirected
    """
    response = client.get("/site/auth-google/")

    assert response.status_code == 302


def test_auth_google_social_authentication_disabled(client):
    """
    GIVEN a Flask client
    WHEN the "/site/auth-google" is requested and social authentication is disabled
    THEN check if client gets redirected to login url
    """
    response = client.get("/site/auth-google/", follow_redirects=True)

    assert response.request.path == "/login/"


# Callback route


def test_callback_redirect_to_error_when_testing_disabled(
    app, client, enable_social_authentication,
):
    """
    GIVEN a Flask app, a Flask client and enabled social authentication
    WHEN testing disabled and the "/login/callback/" is requested
    THEN check if client gets redirected to error 404
    """
    app.config["TESTING"] = False  # disabling testing just for this test
    response = client.get("/login/callback/", follow_redirects=True)

    assert response.request.path == "/error/404/"


def test_callback_redirect_to_signup_from_social_media(
    client, enable_social_authentication,
):
    """
    GIVEN a Flask client and enabled social authentication
    WHEN the "/login/callback/" is requested
    THEN check if client gets redirected to signup from social media
    and session variables are set
    """
    response = client.get("/login/callback/", follow_redirects=True)

    assert response.request.path == "/site/signup-from-social-media/"

    with client.session_transaction() as session:
        assert session.get("google_auth")
        assert session.get("email")


def test_callback_login_already_signed_up_user(
    client, create_test_user, enable_social_authentication,
):
    """
    GIVEN a Flask client, user object, and enabled social authentication
    WHEN the "/login/callback/" is requested
    THEN check if client gets redirected to home
    and user is logged in
    """
    response = client.get("/login/callback/", follow_redirects=True)

    assert response.request.path == "/"

    # If _user_id is present in session - user is logged in
    with client.session_transaction() as session:
        assert session.get("_user_id")


# Signup_from_social_media route


def test_signup_from_social_media_route_template_and_context(
    client,
    captured_templates,
):
    """
    GIVEN a Flask client and captured_templates function
    WHEN the "/site/signup-from-social-media/" page is requested
    THEN check if template used is "authentication/signup_from_social_media.html" and
    form in context is of type GoogleSignupForm
    """
    # Set session variables
    # (required to get access to this route)
    with client.session_transaction() as session:
        session["google_auth"] = True
        session["email"] = "media_user@gmail.com"

    response = client.get("/site/signup-from-social-media/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "authentication/signup_from_social_media.html"
    assert type(context.get("form")) == forms.GoogleSignupForm


def test_signup_from_social_media_route_signup_user(client):
    """
    GIVEN a Flask client
    WHEN a POST request with data is sent to "/site/signup-from-social-media/" page
    THEN check if user got created
    """
    with client.session_transaction() as session:
        session["google_auth"] = True
        session["email"] = "media_user@gmail.com"

    data = {
        "username": "social_media_user",
        "submit": "",
    }

    response = client.post("/site/signup-from-social-media/", data=data)
    assert response.status_code == 302

    assert models.User.objects.first().username == "social_media_user"


def test_signup_from_social_media_route_redirect_no_session_variable(client):
    """
    GIVEN a Flask client
    WHEN no session variable is set and "/site/signup-from-social-media/" page is requested
    THEN check if user gets redirected
    """
    response = client.get("/site/signup-from-social-media/")
    assert response.status_code == 302


# Captcha route


def test_captcha_route(client):
    """
    GIVEN a Flask client
    WHEN the "/site/captcha/reload/" is requested
    THEN check if captcha code is set
    """
    response = client.get("/site/captcha/")
    assert response.status_code == 200

    with client.session_transaction() as session:
        assert session.get("captcha")


def test_captcha_reload_route(client):
    """
    GIVEN a Flask client
    WHEN the "/site/captcha/reload/" is requested
    THEN check if captcha code is updated
    """
    # Load old captcha
    response = client.get("/site/captcha/")
    assert response.status_code == 200

    # Get the old captcha
    with client.session_transaction() as session:
        old_captcha = session.get("captcha")

    # Update the captcha
    response = client.get("/site/captcha/reload/")
    assert response.status_code == 200

    # Check if captcha updated
    with client.session_transaction() as session:
        assert session.get("captcha") != old_captcha
