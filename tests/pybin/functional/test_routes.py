from datetime import datetime, timedelta

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

    assert b"Max amount of tags is 10" in response.data


# Error Route


def test_error_route_template_and_context(client, captured_templates):
    """
    GIVEN a Flask client and captured_templates function
    WHEN the "/error/404/" page is requested
    THEN check if template used is "pybin/error.html"
    """
    response = client.get("/error/404/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/error.html"


# Rating Route


def test_rating_route_like_paste(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "rating" page
    THEN check if paste rating is updated
    """
    # Create a new paste
    new_paste = models.Paste.objects.create(
        content="new paste content",
    )

    data = {
        "data_key": new_paste.uuid_hash,
        "data_rating": "1",
    }

    response = authorized_client.post("/rating/", data=data)
    assert response.status_code == 200

    assert models.Paste.objects.first().rating == 1


def test_rating_route_dislike_paste(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "rating" page
    THEN check if paste rating is updated
    """
    # Create a new paste
    new_paste = models.Paste.objects.create(
        content="new paste content",
    )

    data = {
        "data_key": new_paste.uuid_hash,
        "data_rating": "-1",
    }

    response = authorized_client.post("/rating/", data=data)
    assert response.status_code == 200

    assert models.Paste.objects.first().rating == -1


def test_rating_route_already_liked(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "rating" page
    THEN check if paste rating is updated
    """
    # Create a new paste
    new_paste = models.Paste.objects.create(
        content="new paste content",
    )

    data = {
        "data_key": new_paste.uuid_hash,
        "data_rating": "1",
    }

    response = authorized_client.post("/rating/", data=data)
    assert response.status_code == 200

    response = authorized_client.post("/rating/", data=data)
    assert response.status_code == 200

    assert models.Paste.objects.first().rating == 0


def test_rating_route_already_disliked(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "rating" page
    THEN check if paste rating is updated
    """
    # Create a new paste
    new_paste = models.Paste.objects.create(
        content="new paste content",
    )

    data = {
        "data_key": new_paste.uuid_hash,
        "data_rating": "-1",
    }

    response = authorized_client.post("/rating/", data=data)
    assert response.status_code == 200

    response = authorized_client.post("/rating/", data=data)
    assert response.status_code == 200

    assert models.Paste.objects.first().rating == 0


def test_rating_route_like_after_dislike(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "rating" page
    THEN check if paste rating is updated
    """
    # Create a new paste
    new_paste = models.Paste.objects.create(
        content="new paste content",
    )

    data = {
        "data_key": new_paste.uuid_hash,
        "data_rating": "-1",
    }

    response = authorized_client.post("/rating/", data=data)
    assert response.status_code == 200

    data = {
        "data_key": new_paste.uuid_hash,
        "data_rating": "1",
    }

    response = authorized_client.post("/rating/", data=data)
    assert response.status_code == 200

    assert models.Paste.objects.first().rating == 1


def test_rating_route_dislike_after_like(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "rating" page
    THEN check if paste rating is updated
    """
    # Create a new paste
    new_paste = models.Paste.objects.create(
        content="new paste content",
    )

    data = {
        "data_key": new_paste.uuid_hash,
        "data_rating": "1",
    }

    response = authorized_client.post("/rating/", data=data)
    assert response.status_code == 200

    data = {
        "data_key": new_paste.uuid_hash,
        "data_rating": "-1",
    }

    response = authorized_client.post("/rating/", data=data)
    assert response.status_code == 200

    assert models.Paste.objects.first().rating == -1


def test_rating_route_rate_own_paste(authorized_client, create_test_paste):
    """
    GIVEN an authorized Flask client and Paste object
    WHEN a POST request with own data is sent to "rating" page
    THEN check if paste rating isn't updated
    """
    data = {
        "data_key": create_test_paste.uuid_hash,
        "data_rating": "1",
    }

    response = authorized_client.post("/rating/", data=data)
    assert response.status_code == 200

    assert models.Paste.objects.first().rating == 0


# Document_view Route


def test_document_view_route_template_and_context(
    client,
    captured_templates,
    create_test_paste,
):
    """
    GIVEN a Flask client, captured_templates function and Paste object
    WHEN the "/<uuid_hash>/" page is requested where uuid_hash is paste's uuid_hash
    THEN check if template used is "pybin/document.html" and
    form in context is of type CommentForm
    """
    response = client.get(f"/{create_test_paste.uuid_hash}/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/document.html"
    assert type(context.get("form")) == forms.CommentForm


def test_document_view_route_create_comment_for_paste(
    authorized_client,
    create_test_paste,
):
    """
    GIVEN an authorized Flask client and Paste object
    WHEN a POST request with data is sent to "/<uuid_hash>/" page
    where uuid_hash is paste's uuid_hash
    THEN check if comment got created
    """
    data = {
        "content": "new comment",
        "syntax": "plaintext",
        "submit": "",
    }

    response = authorized_client.post(f"/{create_test_paste.uuid_hash}/", data=data)
    assert response.status_code == 302

    assert len(models.Comment.objects.all()) == 1


def test_document_view_route_create_comment_for_comment(
    authorized_client,
    create_test_comment,
):
    """
    GIVEN an authorized Flask client and Paste object
    WHEN a POST request with data is sent to "/<uuid_hash>/" page
    where uuid_hash is paste's uuid_hash
    THEN check if comment got created
    """
    data = {
        "content": "new comment",
        "syntax": "plaintext",
        "submit": "",
    }

    response = authorized_client.post(f"/{create_test_comment.uuid_hash}/", data=data)
    assert response.status_code == 302

    assert len(models.Comment.objects.all()) == 2


# Document_raw_view Route


def test_document_raw_view_route(client, create_test_paste):
    """
    GIVEN a Flask client and Paste object
    WHEN the "/raw/<uuid_hash>/" page is requested where uuid_hash is paste's uuid_hash
    THEN check if request.data is correct
    """
    response = client.get(f"/raw/{create_test_paste.uuid_hash}/")
    assert response.status_code == 200

    assert f"<pre>{create_test_paste.content}</pre>".encode() in response.data


# Document_delete Route


def test_document_delete_route_delete_paste(authorized_client, create_test_paste):
    """
    GIVEN an authorized Flask client and Paste object
    WHEN a POST request with data is sent to "/delete/<uuid_hash>/" page
    where uuid_hash is paste's uuid_hash
    THEN check if paste got deleted
    """
    response = authorized_client.get(f"/delete/{create_test_paste.uuid_hash}/")
    assert response.status_code == 302

    assert len(models.Paste.objects.all()) == 0


def test_document_delete_route_delete_comment(authorized_client, create_test_comment):
    """
    GIVEN an authorized Flask client and Paste object
    WHEN a POST request with data is sent to "/delete/<uuid_hash>/" page
    where uuid_hash is comment's uuid_hash
    THEN check if comment got deleted
    """
    response = authorized_client.get(f"/delete/{create_test_comment.uuid_hash}/")
    assert response.status_code == 302

    assert models.Comment.objects.first().content == "Comment was deleted"


# Document_edit Route


def test_document_edit_route_template_and_context_paste(
    authorized_client,
    captured_templates,
    create_test_paste,
):
    """
    GIVEN an authroized Flask client and captured_templates function
    WHEN the "/edit/<uuid_hash>/" page is requested
    THEN check if template used is "pybin/edit_paste.html" and
    form in context is of type PasteForm
    """
    response = authorized_client.get(f"/edit/{create_test_paste.uuid_hash}/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/edit_paste.html"
    assert type(context.get("form")) == forms.PasteForm


def test_document_edit_route_template_and_context_comment(
    authorized_client,
    captured_templates,
    create_test_comment,
):
    """
    GIVEN an authroized Flask client and captured_templates function
    WHEN the "/edit/<uuid_hash>/" page is requested
    THEN check if template used is "pybin/edit_comment.html" and
    form in context is of type CommentForm
    """
    response = authorized_client.get(f"/edit/{create_test_comment.uuid_hash}/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/edit_comment.html"
    assert type(context.get("form")) == forms.CommentForm


def test_document_edit_route_edit_paste(authorized_client, create_test_paste):
    """
    GIVEN an authorized Flask client and Paste object
    WHEN a POST request with data is sent to "/edit/<uuid_hash>/" page
    where uuid_hash is paste's uuid_hash
    THEN check if paste got deleted
    """
    data = {
        "content": "edited paste",
        "category": "None",
        "tags": "",
        "syntax": "plaintext",
        "expiration": "0",
        "exposure": "Public",
        "title": "",
        "submit": "",
    }

    response = authorized_client.post(
        f"/edit/{create_test_paste.uuid_hash}/",
        data=data,
    )
    assert response.status_code == 302

    assert models.Paste.objects.first().content == "edited paste"


def test_document_edit_route_edit_paste_more_than_10_tags(
    authorized_client, create_test_paste,
):
    """
    GIVEN an authorized Flask client and Paste object
    WHEN a POST request with data is sent to "/edit/<uuid_hash>/" page
    where uuid_hash is paste's uuid_hash
    THEN check if paste got deleted
    """
    data = {
        "content": "edited paste",
        "category": "None",
        "tags": "1,2,3,4,5,6,7,8,9,10,11",
        "syntax": "plaintext",
        "expiration": "0",
        "exposure": "Public",
        "title": "",
        "submit": "",
    }

    response = authorized_client.post(
        f"/edit/{create_test_paste.uuid_hash}/",
        data=data,
    )
    assert response.status_code == 200

    assert b"Max amount of tags is 10" in response.data


def test_document_edit_route_edit_comment(authorized_client, create_test_comment):
    """
    GIVEN an authorized Flask client and Comment object
    WHEN a POST request with data is sent to "/edit/<uuid_hash>/" page
    where uuid_hash is comment's uuid_hash
    THEN check if comment got edited
    """
    data = {
        "content": "edited comment",
        "syntax": "plaintext",
        "submit": "",
    }

    response = authorized_client.post(
        f"/edit/{create_test_comment.uuid_hash}/",
        data=data,
    )
    assert response.status_code == 302

    assert models.Comment.objects.first().content == "edited comment"


def test_document_edit_route_edit_comment_older_than_5_minutes(
    authorized_client,
    create_test_comment,
):
    """
    GIVEN an authorized Flask client and Comment object older than 5 minutes
    WHEN a POST request with data is sent to "/edit/<uuid_hash>/" page
    where uuid_hash is comment's uuid_hash
    THEN check if comment didn't get edited
    """

    # Make comment older than 5 mintues
    five_minutes_older = datetime.utcnow() - timedelta(minutes=5)

    create_test_comment.created = five_minutes_older
    create_test_comment.save()

    data = {
        "content": "edited comment",
        "syntax": "plaintext",
        "submit": "",
    }

    response = authorized_client.post(
        f"/edit/{create_test_comment.uuid_hash}/",
        data=data,
    )
    assert response.status_code == 302

    assert models.Comment.objects.first().content != "edited comment"
