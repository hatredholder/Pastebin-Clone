from flask import Blueprint, render_template

from flask_login import current_user, login_required


pastebin = Blueprint('pastebin', __name__)


@pastebin.route('/')
def index():
    return render_template('authentication/index.html')


@pastebin.route('/profile')
@login_required
def profile():
    return render_template('authentication/profile.html', name=current_user.name)
