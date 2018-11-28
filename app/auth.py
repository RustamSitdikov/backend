#!/usr/bin/env python

from . import app
from flask import Flask
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint, GitHub

oauth = OAuth(app)


oauth.register('twitter',
    client_id='Twitter Consumer Key',
    client_secret='Twitter Consumer Secret',
    request_token_url='https://api.twitter.com/oauth/request_token',
    request_token_params=None,
    access_token_url='https://api.twitter.com/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    authorize_url='https://api.twitter.com/oauth/authenticate',
    api_base_url='https://api.twitter.com/1.1/',
    client_kwargs=None,
)