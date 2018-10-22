#!/usr/bin/env python

from flask import (Blueprint, request, jsonify, render_template)

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login/', methods={'GET', 'POST'})
def login():
    if request.method == 'POST':
        return jsonify(request.form)

    return render_template('auth/login.html')