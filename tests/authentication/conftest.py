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

    # Enable email verification
    app.config["EMAIL_VERIFICATION_ENABLED"] = True

    yield True

    # Disable email verification on teardown
    app.config["EMAIL_VERIFICATION_ENABLED"] = False


@pytest.fixture
def enable_social_authentication(app):
    """
    Enable social authentication
    (Requires social authentication settings to be set in a .env file)
    """

    # Find and load the .env file
    dotenv_path = os.path.join(
        pathlib.Path(__file__).parent.parent.parent,
        ".env",
    )
    load_dotenv(dotenv_path)

    # Setup the .env file
    app.config.from_prefixed_env()

    # Enable social authentication
    app.config["SOCIAL_AUTHENTICATION_ENABLED"] = True

    yield True

    # Disable social authentication on teardown
    app.config["SOCIAL_AUTHENTICATION_ENABLED"] = False
