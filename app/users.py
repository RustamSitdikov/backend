#!/usr/bin/env python

from flask import (Blueprint, jsonify)
from flask import current_app as app

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/', methods=['GET'])
def get_users():
    return jsonify(users='users')


@users.route('/<string:username>/', methods=['GET'])
def get_user(username=None):
    return jsonify(username=username)