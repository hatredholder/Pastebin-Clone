import pybin.forms as forms
import pybin.models as models
import pybin.utils as utils

import pytest


# Home Route


def test_home_route_template_and_context(client, captured_templates):
    """
    GIVEN a Flask client and captured_templates function
    WHEN the "/" page is requested
    THEN check if template used is "pybin/home.html" and
    form in context is of type PasteForm
    """
    response = client.get("/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/home.html"
    assert type(context.get("form")) == forms.PasteForm


def test_home_route_create_paste_as_guest(client):
    """
    GIVEN a Flask client
    WHEN a POST request with data is sent to "/" page
    THEN check if paste got created and author is None
    """
    data = {
        "content": "new paste",
        "category": "None",
        "tags": "",
        "syntax": "plaintext",
        "expiration": "0",
        "exposure": "Public",
        "title": "",
        "submit": "",
    }

    response = client.post("/", data=data)
    assert response.status_code == 302

    assert len(models.Paste.objects.all()) == 1

    assert models.Paste.objects.first().author is None


def test_home_route_create_paste_authorized(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "/" page
    THEN check if paste got created and author is new_user
    """
    data = {
        "content": "new paste",
        "category": "None",
        "tags": "",
        "syntax": "plaintext",
        "expiration": "0",
        "exposure": "Public",
        "title": "",
        "submit": "",
    }

    response = authorized_client.post("/", data=data)
    assert response.status_code == 302

    assert len(models.Paste.objects.all()) == 1

    assert models.Paste.objects.first().author.username == "new_user"


def test_home_route_create_paste_more_than_10_tags(client):
    """
    GIVEN a Flask client
    WHEN a POST request with incorrect data is sent to "/" page
    THEN check if flash message is displayed
    """
    data = {
        "content": "new paste",
        "category": "None",
        "tags": "1,2,3,4,5,6,7,8,9,10,11",
        "syntax": "plaintext",
        "expiration": "0",
        "exposure": "Public",
        "title": "",
        "submit": "",
    }

    response = client.post("/", data=data)
    assert response.status_code == 200

    assert b'Max amount of tags is 10' in response.data
