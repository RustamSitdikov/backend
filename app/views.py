#!/usr/bin/env python

from app import app
from flask import request, redirect, url_for, jsonify, flash, send_from_directory, render_template
from werkzeug.utils import secure_filename
import os


@app.route('/<string:name>/')
@app.route('/')
def index(name='world'):
    return "Hello, {}!".format(name)