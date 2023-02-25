from flask import Flask

from flask_login import LoginManager

from flask_mail import Mail

from flask_mongoengine import MongoEngine


# Setup app
app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
    "db": "pastebinCloneDb",
    "host": "localhost",
    "port": 27017,
    "username": "rootuser",
    "password": "rootpass",
}
app.config["SECRET_KEY"] = "supersecretkey"
app.config["RECAPTCHA_PUBLIC_KEY"] = "6Lc2biIjAAAAAK_wx4fiQ-mAdd0TQZzHKOPBurBD"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6Lc2biIjAAAAAA_JouXEC1IhL0hp1pxGZxRlEAay"

app.config.from_prefixed_env()

# Setup MongoEngine
db = MongoEngine()
db.init_app(app)

# Setup LoginManager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

# Setup Flask-Mail
mail = Mail(app)


# User-loader callback
# (flask-login.readthedocs.io/en/latest/#how-it-works)
@login_manager.user_loader
def load_user(user_id):
    from authentication.models import (
        User,
    )  # import in-function to avoid circular import

    return User.objects(id=user_id).first()


# Register blueprints to get the routes working
from authentication.routes import auth as auth_blueprint  # noqa: E402, I100

app.register_blueprint(auth_blueprint)

from pybin.routes import pybin as pb_blueprint  # noqa: E402

app.register_blueprint(pb_blueprint)

# Import context processors to make them available in templates
import pybin.context_processors  # noqa: E402, F401, I202, I100 <- damn that's a lot of errors

# Import timesince filter to make it available in templates as well
from pybin.utils import timesince  # noqa: E402, F401, I202
