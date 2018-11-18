#!/usr/bin/env python

from flask import Flask
from flask_jsonrpc import JSONRPC

import boto3

# Define application
app = Flask(__name__, instance_relative_config=True)
jsonrpc = JSONRPC(app, '/api/')

# s3_session = boto3.session.Session()
# s3_client = s3_session.client()

# Load the default configuration
app.config.from_object('config.DevelopmentConfig')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py', silent=True)

# Import views
from .views import *

# # Import model
# from .model import create_personal_chat, list_chats
#
# print(create_personal_chat(1))
# exit()
