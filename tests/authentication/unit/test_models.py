# import pytest


def test_user_model_str_method(create_test_user):
    assert str(create_test_user) == "<User new_user>"


def test_user_model_clean_method(db, create_test_user):
    assert create_test_user.avatar
