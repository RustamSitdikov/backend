#!/usr/bin/env python

"""
Simple gunicorn spplication
"""

import json
from datetime import datetime
import gunicorn.app.base
from gunicorn.six import iteritems


def number_of_workers():
    return 1


def handler_app(environ, start_response):
    response_body = str({
        "time": datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"),
        "url": 'https://github.com'
    }).encode('utf-8')
    status = '200 OK'

    response_headers = [
        ('Content-Type', 'application/json'),
    ]

    start_response(status, response_headers)

    return [response_body]


class Application(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(Application, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    host = '127.0.0.1'
    post = '8080'
    options = {
        'bind': '%s:%s' % (host, post),
        'workers': number_of_workers(),
    }
    Application(handler_app, options).run()
