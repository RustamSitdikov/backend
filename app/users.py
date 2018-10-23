#!/usr/bin/env python

from flask import (Blueprint, jsonify, request)
from flask import current_app as app

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/list/', methods=['GET'])
@users.route('/list/<string:query>/', methods=['GET'])
@users.route('/list/<string:query>/<int:limit>', methods=['GET'])
def get_users(query=None, limit=None):
    return jsonify({"users":["User1", "User2", "User3"]})