import os
from flask import redirect, url_for, session, render_template
from flask_oauth import OAuth
from easypc import app
from functools import wraps

oauth = OAuth()
twitter = oauth.remote_app(
    'twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=(os.environ.get('TWITTER_KEY')),
    consumer_secret=(os.environ.get('TWITTER_SECRET'))
)


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


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/oauth2callback')
@twitter.authorized_handler
def oauth_authorized(resp):
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['user'] = "twitter:%s" % resp['screen_name']
    return redirect(url_for('index'))


@app.route('/login/twitter')
def login_twitter():
    if "twitter_token" in session:
        del session['twitter_token']

    return twitter.authorize(callback=url_for('oauth_authorized'))
