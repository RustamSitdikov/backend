#!/usr/bin/env python

from flask import Flask

# Defina application
app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.DevelopmentConfig')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# Import blueprints
from .auth import auth
app.register_blueprint(auth)

from .chats import chats
app.register_blueprint(chats)

from .users import users
app.register_blueprint(users)

# Import views
from .views import *
