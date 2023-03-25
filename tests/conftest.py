
from flask_mongoengine import MongoEngine

import mongoengine

import pytest


@pytest.fixture
def app():
    """
    Setup Flask app for testing
    """
    from app import app

    app.config["TESTING"] = True  # enable testing
    app.config["WTF_CSRF_ENABLED"] = False  # disable csrf for forms

    mongoengine.connection.disconnect_all()

    # Use app_context
    # (https://flask.palletsprojects.com/en/2.2.x/testing/#tests-that-depend-on-an-active-context)
    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    """
    Setup Mongoengine Database
    """

    # Setup test Mongo database credentials
    app.config["MONGODB_SETTINGS"] = [
        {
            "db": "pastebin_test_db",
            "host": "localhost",
            "port": 27017,
        },
    ]

    # Setup db MongoEngine variable
    db = MongoEngine(app)

    # Teardown (clear database before tests)
    db.connection["default"].drop_database("pastebin_test_db")

    # Send the variable
    yield db

    # Teardown (clear database after tests)
    db.connection["default"].drop_database("pastebin_test_db")
