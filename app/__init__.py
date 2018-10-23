#!/usr/bin/env python

from flask import Flask

# Define application
app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.DevelopmentConfig')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py', silent=True)

# Import views
from .views import *
