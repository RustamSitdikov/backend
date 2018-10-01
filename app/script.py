#!/usr/bin/env python

"""
Simple flask spplication
"""

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
	"""
	Print "Hello, world!" in browser.
	"""
	return "Hello, World!"
