from flask import redirect, url_for, session, render_template
from easypc import app
from functools import wraps

from easypc.lib.oauth import facebook, twitter


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session or session['user'] is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/")
@login_required
def index():
    return redirect(url_for('list'))
