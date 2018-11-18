#!/usr/bin/env python

from flask import Flask
from flask_jsonrpc import JSONRPC
from config import Config

import boto3

# Define application
app = Flask(__name__, instance_relative_config=True)
jsonrpc = JSONRPC(app, '/api/')

s3_session = boto3.session.Session()
s3_client = s3_session.client(service_name=Config.S3_SERVICE_NAME, endpoint_url=Config.S3_ENDPOINT_URL,
                              aws_access_key_id=Config.S3_ACCESS_KEY_ID, aws_secret_access_key=Config.S3_SECRET_ACCESS_KEY)

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
