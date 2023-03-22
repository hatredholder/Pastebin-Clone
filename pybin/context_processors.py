import datetime

from app import app

from flask_login import current_user

import pybin.utils as utils


@app.context_processor
def profile_image():
    """Returns a pre-formatted base64 user's avatar image data for HTML templates"""

    def __profile_image(user):
        avatar = utils.create_base64_img_data(user)
        return avatar

    return dict(profile_image=__profile_image)


@app.context_processor
def my_pastes():
    """Returns a list of pastes made by current_user"""

    def __my_pastes():
        pastes = utils.get_my_pastes(current_user)
        return pastes

    return dict(my_pastes=__my_pastes)


@app.context_processor
def public_pastes():
    """Returns a list of public pastes"""

    def __public_pastes():
        pastes = utils.get_public_pastes(current_user)
        return pastes

    return dict(public_pastes=__public_pastes)


@app.context_processor
def comment_older_than_5_minutes():
    """Returns True if comment is older than 5 minutes"""

    def __comment_older_than_5_minutes(document):
        if document.created + datetime.timedelta(minutes=5) < datetime.datetime.now():
            return True

    return dict(comment_older_than_5_minutes=__comment_older_than_5_minutes)
