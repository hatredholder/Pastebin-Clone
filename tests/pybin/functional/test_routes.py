from datetime import datetime, timedelta

from authentication.models import User

import pybin.forms as forms
import pybin.models as models


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


def test_document_view_route_5_minute_old_comment(
    authorized_client,
    create_test_comment,
):
    """
    GIVEN a Flask client and a Comment object
    WHEN the "/<uuid_hash>/" page is requested where uuid_hash is comment's uuid_hash
    THEN check if edit button is gone
    """
    # Make comment older than 5 mintues
    five_minutes_older = datetime.utcnow() - timedelta(minutes=5)

    create_test_comment.created = five_minutes_older
    create_test_comment.save()

    response = authorized_client.get(f"/{create_test_comment.uuid_hash}/")
    assert response.status_code == 200

    assert b'edit' not in response.data


def test_document_view_route_incorrect_hash(client):
    """
    GIVEN a Flask client and a Paste object
    WHEN the "/<uuid_hash>/" page is requested where uuid_hash is incorrect uuid_hash
    THEN check if user gets redirected
    """
    response = client.get("/incorrect_hash/")
    assert response.status_code == 302


def test_document_view_route_expired_paste(client, create_test_paste):
    """
    GIVEN a Flask client and a expired Paste object
    WHEN the "/<uuid_hash>/" page is requested where uuid_hash is paste's uuid_hash
    THEN check if user gets redirected and paste is deleted
    """
    # Make paste an hour older
    one_hour_older = datetime.utcnow() - timedelta(hours=1)
    create_test_paste.created = one_hour_older

    # Set expiration to an hour
    create_test_paste.expiration = 3600
    create_test_paste.save()

    response = client.get(f"/{create_test_paste.uuid_hash}/")

    assert response.status_code == 302
    assert len(models.Paste.objects.all()) == 0


def test_document_view_route_private_paste(client, create_test_paste):
    """
    GIVEN a Flask client and a expired Paste object
    WHEN the "/<uuid_hash>/" page is requested where uuid_hash is private paste's uuid_hash
    THEN check if user gets redirecte
    """
    create_test_paste.exposure = "Private"
    create_test_paste.save()

    response = client.get(f"/{create_test_paste.uuid_hash}/")

    assert response.status_code == 302


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
    WHEN a request is sent to "/delete/<uuid_hash>/" page
    where uuid_hash is paste's uuid_hash
    THEN check if paste got deleted
    """
    response = authorized_client.get(f"/delete/{create_test_paste.uuid_hash}/")
    assert response.status_code == 302

    assert len(models.Paste.objects.all()) == 0


def test_document_delete_route_delete_paste_not_author(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a request is sent to "/delete/<uuid_hash>/" page
    THEN check if paste didn't get deleted
    """
    new_paste = models.Paste.objects.create(
        content="new paste content",
    )
    new_paste.save()

    response = authorized_client.get(f"/delete/{new_paste.uuid_hash}/")
    assert response.status_code == 302

    assert len(models.Paste.objects.all()) == 1


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
    authorized_client,
    create_test_paste,
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


# Document_clone Route


def test_document_clone_route_template_and_context(
    authorized_client,
    captured_templates,
    create_test_paste,
):
    """
    GIVEN an authroized Flask client and captured_templates function
    WHEN the "/clone/<uuid_hash>/" page is requested
    THEN check if template used is "pybin/clone_document.html" and
    form in context is of type PasteForm
    """
    response = authorized_client.get(f"/clone/{create_test_paste.uuid_hash}/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/clone_document.html"
    assert type(context.get("form")) == forms.PasteForm


# Message_view Route


def test_message_view_route_template_and_context(
    authorized_client,
    captured_templates,
    create_test_message,
):
    """
    GIVEN a Flask client and captured_templates function
    WHEN the "/message/<uuid_hash>" page is requested
    THEN check if template used is "pybin/message.html" and
    form in context is of type MessageForm
    """
    response = authorized_client.get(f"/message/{create_test_message.uuid_hash}/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/message.html"
    assert type(context.get("form")) == forms.MessageForm


def test_message_view_route_incorrect_hash(
    authorized_client,
):
    """
    GIVEN a Flask client and captured_templates function
    WHEN the "/message/<uuid_hash>" page is requested
    THEn check if user is redirected
    """
    response = authorized_client.get("/message/incorrect_hash/")
    assert response.status_code == 302


def test_message_view_route_create_reply(
    authorized_client,
    captured_templates,
    create_test_message,
):
    """
    GIVEN a Flask client
    WHEN a POST request with data is sent to "/" page
    THEN check if paste got created and author is None
    """
    data = {
        "content": "new reply",
        "submit": "",
    }

    response = authorized_client.post(
        f"/message/{create_test_message.uuid_hash}/",
        data=data,
    )
    assert response.status_code == 302

    assert len(models.Message.objects.first().replies) == 1


# Send_message Route


def test_send_message_route_template_and_context(authorized_client, captured_templates):
    """
    GIVEN a Flask client and captured_templates function
    WHEN the "/message/compose/" page is requested
    THEN check if template used is "pybin/send_message.html"
    """
    response = authorized_client.get("/message/compose/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/send_message.html"


# Reply_delete Route


def test_reply_delete_route_delete_reply(
    authorized_client,
    create_test_message,
    create_test_reply,
):
    """
    GIVEN an authorized Flask client and Paste object
    WHEN a request is sent to "/reply/delete/<message_hash>/<reply_hash>/" page
    THEN check if reply got deleted
    """
    create_test_message.replies.append(create_test_reply)
    create_test_message.save()

    response = authorized_client.get(
        f"/reply/delete/{create_test_message.uuid_hash}/{create_test_reply.uuid_hash}/",
    )
    assert response.status_code == 302

    assert len(models.Message.objects.first().replies) == 0


# My_pybin Route


def test_my_pybin_route_template_and_context(
    client, captured_templates, create_test_user,
):
    """
    GIVEN a Flask client, captured_templates function and a user object
    WHEN the "/u/<username>/" page is requested
    THEN check if template used is "pybin/my_pybin.html"
    """
    response = client.get(f"/u/{create_test_user.username}/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/my_pybin.html"


def test_my_pybin_route_redirect_incorrect_username(client):
    """
    GIVEN a Flask client function
    WHEN the "/u/<username>/" page is requested where username is incorrect
    THEN check if user is redirected
    """
    response = client.get("/u/incorrect_username/")
    assert response.status_code == 302


# My_comments Route


def test_my_comments_route_template_and_context(
    authorized_client, captured_templates, create_test_user,
):
    """
    GIVEN a Flask client, captured_templates function and a user object
    WHEN the "/u/<username>/comments/" page is requested
    THEN check if template used is "pybin/my_comments.html"
    """
    response = authorized_client.get(f"/u/{create_test_user.username}/comments/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/my_comments.html"


def test_my_comments_route_redirect_incorrect_username(authorized_client):
    """
    GIVEN an authorized Flask client function
    WHEN the "/u/<username>/comments" page is requested where username is incorrect
    THEN check if user is redirected
    """
    response = authorized_client.get("/u/incorrect_username/comments/")
    assert response.status_code == 302


# My_messages Route


def test_my_messages_route_template_and_context(authorized_client, captured_templates):
    """
    GIVEN a Flask client and captured_templates function
    WHEN the "/messages/" page is requested
    THEN check if template used is "pybin/my_messages.html"
    """
    response = authorized_client.get("/messages/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/my_messages.html"


# Profile Route


def test_profile_route_template_and_context(authorized_client, captured_templates):
    """
    GIVEN an authorized Flask client and captured_templates function
    WHEN the "/user/profile/" page is requested
    THEN check if template used is "pybin/edit_profile.html" and
    form in context is of type ProfileForm
    """
    response = authorized_client.get("/user/profile/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/edit_profile.html"
    assert type(context.get("form")) == forms.ProfileForm


def test_profile_route_set_email(authorized_client, create_test_user):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "/user/profile/" page
    THEN check if profile got updated
    """
    data = {
        "email": "brand_new_email@gmail.com",
        "location": "",
        "website_url": "",
        "submit": "",
    }

    response = authorized_client.post("/user/profile/", data=data)
    assert response.status_code == 302

    assert User.objects.first().email == "brand_new_email@gmail.com"
    assert User.objects.first().email_verified == False  # noqa: E712


def test_profile_route_update_email_already_taken(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "/user/profile/" page
    THEN check if flash message is displayed
    """
    user_with_already_taken_email = User(
        username="taken_email",
        email="taken_email@gmail.com",
        password_hash="taken_email_password",
    )
    user_with_already_taken_email.save()

    data = {
        "email": "taken_email@gmail.com",
        "website_url": "",
        "location": "",
        "submit": "",
    }

    response = authorized_client.post("/user/profile/", data=data)
    assert response.status_code == 200

    assert b"This email address has already been taken." in response.data


def test_profile_route_set_incorrect_website_url(authorized_client, create_test_user):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "/user/profile/" page
    THEN check if flash message is displayed
    """
    data = {
        "email": create_test_user.email,
        "website_url": "google.com",
        "location": "",
        "submit": "",
    }

    response = authorized_client.post("/user/profile/", data=data)
    assert response.status_code == 200

    assert b"Please make sure your website starts with http:// or https://" in response.data


# Avatar Route


def test_avatar_route_template_and_context(authorized_client, captured_templates):
    """
    GIVEN an authorized Flask client and captured_templates function
    WHEN the "/user/change-avatar/" page is requested
    THEN check if template used is "pybin/avatar.html"
    """
    response = authorized_client.get("/user/change-avatar/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/avatar.html"
    assert type(context.get("form")) == forms.AvatarForm


def test_avatar_route_update_avatar(authorized_client):
    """
    GIVEN an authorized Flask client
    WHEN a POST request with data is sent to "/" page
    THEN check if paste got created and author is None
    """
    data = {
        "avatar": open("static/img/guest.png", "rb"),  # noqa: SIM115
        "submit": "",
    }

    response = authorized_client.post("/user/change-avatar/", data=data)
    assert response.status_code == 302


# Search_pastes Route


def test_search_pastes_route_template_and_context(authorized_client, captured_templates):
    """
    GIVEN an authorized Flask client and captured_templates function
    WHEN the "/search/" page is requested
    THEN check if template used is "pybin/search_pastes.html"
    """
    response = authorized_client.get("/search/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template, context = captured_templates[0]

    assert template.name == "pybin/search_pastes.html"


def test_search_pastes_route_with_search_query(authorized_client, create_test_paste):
    """
    GIVEN an authorized Flask client and captured_templates function
    WHEN the "/search/" page is requested
    THEN check if template used is "pybin/search_pastes.html"
    """
    response = authorized_client.get("/search/?q=untitled")
    assert response.status_code == 200

    assert b'test paste' in response.data
