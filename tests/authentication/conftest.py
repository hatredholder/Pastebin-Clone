import os
import pathlib

import authentication.models as models

from dotenv import load_dotenv

import pytest

from werkzeug.security import generate_password_hash


@pytest.fixture
def create_test_user(db):
    """
    Create and return a User object
    """
    new_user = models.User(
        username="new_user",
        email="new_user@gmail.com",
        password_hash=generate_password_hash("new_user_password"),
        email_verified=True,
    )
    new_user.save()

    return new_user


@pytest.fixture
def enable_email_verification(app):
    """
    Enable email verification
    (Requires email settings to be set in a .env file)
    """

    # Find and load the .env file
    dotenv_path = os.path.join(
        pathlib.Path(__file__).parent.parent.parent,
        ".env",
    )
    load_dotenv(dotenv_path)

    # Setup the .env file
    app.config.from_prefixed_env()
