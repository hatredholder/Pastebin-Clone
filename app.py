from flask import Flask

from flask_mongoengine import MongoEngine

# from flask_login import LoginManager


def create_app():
    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {
        'db': 'pastebinCloneDb',
        'host': 'localhost',
        'port': 27017,
    }
    app.config['SECRET_KEY'] = 'supersecretkey'

    db = MongoEngine()
    db.init_app(app)

    from authentication import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from pastebin import pastebin as pb_blueprint
    app.register_blueprint(pb_blueprint)

    return app
