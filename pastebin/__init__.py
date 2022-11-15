from flask import Blueprint, render_template


pastebin = Blueprint('pastebin', __name__)


@pastebin.route('/')
def index():
    return render_template('index.html')


@pastebin.route('/')
def profile():
    return render_template('profile.html')
