import authentication.forms as forms
import authentication.models as models


def test_signup_route_template_used(client, captured_templates):
    """
    GIVEN a Flask client and captured_templates function
    WHEN the '/signup/' page is requested
    THEN check if template used is 'authentication/signup.html' and
    form in context is of type SignupForm
    """
    response = client.get("/signup/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "authentication/signup.html"
    assert type(context["form"]) == forms.SignupForm


def test_signup_route_signup_user(client, db):
    response = client.get("/site/captcha/")

    with client.session_transaction() as session:
        data = {
            "username": "new_signup_user",
            "email": "new_signup_user@gmail.com",
            "password": "new_signup_password",
            "captcha": session["captcha"],
            "submit": "",
        }

    response = client.post("/signup/", data=data)

    assert response.status_code == 302
    assert len(models.User.objects.all()) == 2
