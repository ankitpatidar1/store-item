import os
from flask import g
from flask_oauthlib.client import OAuth

oauth = OAuth()

github = oauth.remote_app(
    'github',
    consumer_key=os.getenv('GITHUB_CONSUMER_KEY'),
    consumer_secret=os.getenv('GITHUB_CONSUMER_SECRET'),
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    access_token_method='POST',
    request_token_url=None,
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

@github.tokengetter
def get_github_token():
    if 'access_token' in g:
        return g.access_token


facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=os.getenv('FACEBOOK_CONSUMER_KEY'),
    consumer_secret=os.getenv('FACEBOOK_CONSUMER_SECRET'),
    request_token_params={'scope': 'email'}
)

@facebook.tokengetter
def get_facebook_token():
    if 'access_token' in g:
        return g.access_token