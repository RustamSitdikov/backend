#!/usr/bin/env python

from . import app
from flask import g, session, request, url_for, flash, jsonify, redirect
from flask_oauthlib.client import OAuth

oauth = OAuth(app)

github = oauth.remote_app(
    'github',
    app_key='backend',
    consumer_key='4db1ce1afb2316bb26d8',
    consumer_secret='e864229acc081cd628af908b9fba28928659c4b7',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'

)


@github.tokengetter
def get_github_token():
    if 'github_oauth' in session:
        resp = session['github_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@app.before_request
def before_request():
    g.user = None
    if 'github_oauth' in session:
        g.user = session['github_oauth']


@app.route('/')
def index():
    if 'github_token' in session:
        me = github.get('user')
        return jsonify(me.data)
    return redirect(url_for('login'))


@app.route('/login')
def login():
    callback_url = url_for('authorized', next=request.args.get('next'))
    return github.authorize(callback=callback_url or request.referrer or None)


@app.route('/logout')
def logout():
    session.pop('github_oauth', None)
    return redirect(url_for('index'))


@app.route('/authorized')
def authorized():
    resp = github.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['github_token'] = (resp['access_token'], '')
    me = github.get('user')
    print(me)
    return jsonify(me.data)


# # Credentials you get from registering a new application
# client_id = '<the id you get from github>'
# client_secret = '<the secret you get from github>'
#
# # OAuth endpoints given in the GitHub API documentation
# authorization_base_url = 'https://github.com/login/oauth/authorize'
# token_url = 'https://github.com/login/oauth/access_token'
#
# from requests_oauthlib import OAuth2Session
# github = OAuth2Session(client_id)
#
# # Redirect user to GitHub for authorization
# authorization_url, state = github.authorization_url(authorization_base_url)
# print('Please go here and authorize,', authorization_url)
#
# # Get the authorization verifier code from the callback url
# redirect_response = raw_input('Paste the full redirect URL here:')
#
# # Fetch the access token
# github.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)
#
# # Fetch a protected resource, i.e. user profile
# r = github.get('https://api.github.com/user')
# print(r.content)


# github = OAuth(app).remote_app(
#     'github',
#     app_key='backend',
#     consumer_key='4db1ce1afb2316bb26d8',
#     consumer_secret='e864229acc081cd628af908b9fba28928659c4b7',
#     request_token_params={'scope': 'user:email'},
#     base_url='https://api.github.com/',
#     request_token_url=None,
#     access_token_method='POST',
#     access_token_url='https://github.com/login/oauth/access_token',
#     authorize_url='https://github.com/login/oauth/authorize'
#
# )
#
#
# @app.route('/')
# def index():
#     if 'github_token' in session:
#         me = github.get('user')
#         return jsonify(me.data)
#     return redirect(url_for('login'))
#
#
# @app.route('/login')
# def login():
#     return redirect(url_for('authorized'))
#     # return github.authorize(callback=url_for('authorized', _external=True))
#
#
# @app.route('/logout')
# def logout():
#     session.pop('github_token', None)
#     return redirect(url_for('index'))
#
#
# @app.route('/login/authorized')
# def authorized():
#     resp = github.authorized_response()
#     if resp is None or resp.get('access_token') is None:
#         return 'Access denied: reason=%s error=%s resp=%s' % (
#             request.args['error'],
#             request.args['error_description'],
#             resp
#         )
#     session['github_token'] = (resp['access_token'], '')
#     me = github.get('user')
#     print(me)
#     return jsonify(me.data)
#
#
# @github.tokengetter
# def get_github_oauth_token():
#     return session.get('github_token')
