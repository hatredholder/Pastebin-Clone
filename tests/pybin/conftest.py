import pybin.models as models

import pytest

from tests.authentication.conftest import create_test_user  # noqa: F401


@pytest.fixture
def create_test_paste(db, create_test_user):  # noqa: F811
    """
    Create and return a Paste object
    """
    new_paste = models.Paste(
        content="test paste",
        author=create_test_user,
    )
    new_paste.save()

    return new_paste


@pytest.fixture
def create_test_comment(db, create_test_user):  # noqa: F811
    """
    Create, save and return a Comment object
    """
    new_comment = models.Comment(
        content="test comment",
        author=create_test_user,
    )
    new_comment.save()

    return new_comment


@pytest.fixture
def create_test_message(db, create_test_user):  # noqa: F811
    """
    Create, save and return a Message object
    """
    new_message = models.Message(
        content="test message",
        author=create_test_user,
        receiver=create_test_user,
    )
    new_message.save()

    return new_message


@pytest.fixture
def create_test_reply(db, create_test_user):  # noqa: F811
    """
    Create and return a Reply object
    """
    new_reply = models.Reply(
        content="test reply",
        author=create_test_user,
    )

    return new_reply
