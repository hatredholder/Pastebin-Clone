import authentication.forms as forms
import authentication.models as models


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
    assert type(context["form"]) == forms.SignupForm


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
            "captcha": session["captcha"],  # get generated captcha code
            "submit": "",
        }

    response = client.post("/signup/", data=data)
    assert response.status_code == 302

    assert models.User.objects.first().username == "new_signup_user"


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
    assert b'The verification code is incorrect.' in response.data


def test_signup_route_signup_user_already_used_username(client, create_test_user):
    """
    GIVEN a Flask client
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
            "captcha": session["captcha"],  # get generated captcha code
            "submit": "",
        }

    response = client.post("/signup/", data=data)
    assert response.status_code == 200

    assert b'This username has already been taken.' in response.data


def test_signup_route_signup_user_already_used_email(client, create_test_user):
    """
    GIVEN a Flask client
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
            "captcha": session["captcha"],  # get generated captcha code
            "submit": "",
        }

    response = client.post("/signup/", data=data)
    assert response.status_code == 200

    assert b'Email address already exists.' in response.data


# def test_signup_route_signup_user_email_verification_enabled(client, enable_email_verification):
    # TODO: Write this test later when I feel like doing it

    # """
    # GIVEN a Flask client
    # WHEN a POST request with data is sent to "/signup/" page
    # THEN check if user got created
    # """
    # # Access "/site/captcha" to generate a captcha code
    # response = client.get("/site/captcha/")
    # assert response.status_code == 200
    #
    # with client.session_transaction() as session:
    #     data = {
    #         "username": "new_signup_user",
    #         "email": "new_signup_user@gmail.com",
    #         "password": "new_signup_password",
    #         "captcha": session["captcha"],  # get generated captcha code
    #         "submit": "",
    #     }
    #
    # response = client.post("/signup/", data=data)
    # assert response.status_code == 302
    #
    # assert not models.User.objects.first().email_verified


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
    assert type(context["form"]) == forms.LoginForm


def test_login_route_login_user(client, create_test_user):
    """
    GIVEN a Flask client
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
        assert session["_user_id"]


def test_login_route_login_user_incorrect_password(client, create_test_user):
    """
    GIVEN a Flask client
    WHEN a POST request with incorrect password data of create_test_user is sent to "/login/" page
    THEN check if user got logged in
    """
    data = {
        "username": "new_user",
        "password": "new_user_incorrect_password",
        "submit": "",
    }

    response = client.post("/login/", data=data)
    assert response.status_code == 200

    assert b'Please check your login details and try again.' in response.data


def test_login_route_login_user_email_unverified(client, create_test_user):
    """
    GIVEN a Flask client
    WHEN a POST request with incorrect password data of create_test_user is sent to "/login/" page
    THEN check if user got logged in
    """
    # Set email_verified to False and save
    create_test_user.email_verified = False
    create_test_user.save()

    data = {
        "username": "new_user",
        "password": "new_user_password",
        "submit": "",
    }

    response = client.post("/login/", data=data)
    assert response.status_code == 200

    assert b'This account is not activated yet.' in response.data
