import requests
import os
from flask import redirect, url_for, session
from flask_oauth import OAuth
from easypc import app

oauth = OAuth()

google = oauth.remote_app(
    'google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'
    },
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=(os.environ.get('GOOGLE_CLIENT_ID')),
    consumer_secret=(os.environ.get('GOOGLE_SECRET'))
)


@app.route('/login/google')
def login_google():
    if "google_token" in session:
        del session['google_token']
    callback = "%s%s" % (os.environ.get("OAUTH_REDIRECT_HOST"),
                        ('oauth_authorized_google'))
    return google.authorize(callback=callback)


@app.route('/oauth2callback/google')
@google.authorized_handler
def oauth_authorized_google(resp):
    session['google_token'] = (resp['access_token'], resp['access_token'])
    headers = {"Authorization": "OAuth %s" % resp['access_token']}

    data = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                        headers=headers).json
    session['user'] = "google:%s" % data['email']
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('google_token')
