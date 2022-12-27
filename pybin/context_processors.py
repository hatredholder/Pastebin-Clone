from app import app

from flask_login import current_user

import pybin.utils as utils


@app.context_processor
def profile_image():
    def __profile_image():
        avatar = utils.create_base64_img_data()
        return avatar

    return dict(profile_image=__profile_image)


@app.context_processor
def my_pastes():
    def __my_pastes():
        pastes = utils.get_my_pastes(current_user)
        return pastes

    return dict(my_pastes=__my_pastes)


@app.context_processor
def public_pastes():
    def __public_pastes():
        pastes = utils.get_public_pastes(current_user)
        return pastes

    return dict(public_pastes=__public_pastes)
