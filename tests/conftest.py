from flask import Flask

from flask_mongoengine import MongoEngine

import mongoengine

import pytest


@pytest.fixture()
def app():
    """
    Setup Flask app for testing
    """

    app = Flask(__name__)

    app.config["TESTING"] = True  # enable testing
    app.config["WTF_CSRF_ENABLED"] = False  # disable csrf for forms

    mongoengine.connection.disconnect_all()

    # Use app_context
    with app.app_context():
        yield app


@pytest.fixture()
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

    # Send the variable
    yield db

    # Teardown (clear database after tests)
    db.connection["default"].drop_database("pastebin_test_db")
