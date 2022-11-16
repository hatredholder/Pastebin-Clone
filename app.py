from flask import Flask

from flask_login import LoginManager

from flask_mongoengine import MongoEngine


# Setup app
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'pastebinCloneDb',
    'host': 'localhost',
    'port': 27017,
    'username': 'rootuser',
    'password': 'rootpass',
}
app.config['SECRET_KEY'] = 'supersecretkey'

# Setup MongoEngine
db = MongoEngine()
db.init_app(app)

# Setup LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


# User-loader callback
# (flask-login.readthedocs.io/en/latest/#how-it-works)
@login_manager.user_loader
def load_user(user_id):
    from authentication.models import User  # import in-function to avoid circular import

    return User.objects(_id=user_id).first()
    

# Register blueprints to get the routes working
from authentication import auth as auth_blueprint  # noqa: E402, I100
app.register_blueprint(auth_blueprint)

from pastebin import pastebin as pb_blueprint  # noqa: E402
app.register_blueprint(pb_blueprint)
