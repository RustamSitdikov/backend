#!/usr/bin/env python

from flask import Flask
from flask_jsonrpc import JSONRPC
import boto3
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

# Define application
app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.DevelopmentConfig')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py', silent=True)

# S3
s3_session = boto3.session.Session()
s3_client = s3_session.client(service_name=app.config['S3_SERVICE_NAME'],
                              endpoint_url=app.config['S3_ENDPOINT_URL'],
                              aws_access_key_id=app.config['S3_ACCESS_KEY_ID'],
                              aws_secret_access_key=app.config['S3_SECRET_ACCESS_KEY'])

# JSON-RPC
jsonrpc = JSONRPC(app, '/api')

# Import oauth
from .auth import *

# Import cent
# from .cent import cent

# Import model
from .model import *

# Import views
from .views import *

# # Import database
# from app import db
#
# db.create_all()
