#!/usr/bin/env python

from flask import (Blueprint, jsonify, request)
from flask import current_app as app

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/', methods=['GET'])
def get_users():
    if request.method == 'GET':
        query = request.args.get('query', '')
        limit = request.args.get('limit', 10)
        users = dict(users=["User1", "User2", "User3"])
        return jsonify(users=users)


@users.route('/<string:username>/', methods=['GET'])
def get_user(username=None):
    return jsonify(username=username)