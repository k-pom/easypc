import os
from flask import redirect, url_for, session
from flask_oauth import OAuth
from easypc import app

oauth = OAuth()
facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=(os.environ.get('FACEBOOK_KEY')),
    consumer_secret=(os.environ.get('FACEBOOK_SECRET')),
    request_token_params={'scope': 'email'}
)


@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('facebook_token')


@app.route('/oauth2callback/facebook')
@facebook.authorized_handler
def oauth_authorized_facebook(resp):
    session['facebook_token'] = (resp['access_token'], resp['access_token'])
    data = facebook.get('/me?fields=name,email').data
    session['user'] = "facebook:%s" % data['email']
    return redirect(url_for('index'))


@app.route('/login/facebook')
def login_facebook():
    if "facebook_token" in session:
        del session['facebook_token']
    callback = "http://localhost:5000%s" % url_for('oauth_authorized_facebook')
    return facebook.authorize(callback=callback)
