import authentication.models as models

import pytest


@pytest.fixture()
def create_test_user(db):
    """
    Create and return a User object
    """
    new_user = models.User(username="new_user", email="new_user@gmail.com")
    new_user.save()

    return new_user
