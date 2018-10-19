#!/usr/bin/env python

from flask import Flask
import os

STATIC_FOLDER = 'public'
UPLOAD_FOLDER = os.path.join(os.getcwd(), STATIC_FOLDER)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

from .views import *
