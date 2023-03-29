from flask import template_rendered

from flask_login import FlaskLoginClient

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
    app.config["SECRET_KEY"] = "test_key"

    app.test_client_class = FlaskLoginClient

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


@pytest.fixture
def client(app, db):
    """
    Returns Flask test client to send requests with
    """
    # NOTE: db fixture is required for public_pastes() method used in templates
    return app.test_client()


@pytest.fixture
def authorized_client(app, db, create_test_user):
    """
    Returns an authorized Flask test client to send requests with
    """
    # NOTE: db fixture is required for public_pastes() method used in templates
    return app.test_client(user=create_test_user)


@pytest.fixture
def captured_templates(app):
    """
    Returns a list of tuples (returns 1 tuple if route uses 1 template)
    which contains used template and context
    """
    recorded = []

    def record(sender, template, context, **extra):
        # Add a tuple to the list
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        # Send the list
        yield recorded
    finally:
        # Disconnect when finished
        template_rendered.disconnect(record, app)
