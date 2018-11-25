#!/usr/bin/env python

import flask
import psycopg2
from psycopg2 import extras
from contextlib import closing
from functools import wraps
import logging
import os
from app import app

DB_CONNECTION = "dbconnection"


def connection():
    if not hasattr(flask.g, DB_CONNECTION):
        flask.g.dbconnection = psycopg2.connect(
            database=app.config['DATABASE_NAME'],
            user=app.config['DATABASE_USER'], password=app.config['DATABASE_PASSWORD'],
            host=app.config['DATABASE_HOST']
        )
    return flask.g.dbconnection


def close():
    if hasattr(flask.g, DB_CONNECTION):
        conn = flask.g.dbconnection
        conn.close()
        delattr(flask.g, DB_CONNECTION)


def cursor():
    with connection() as conn:
        return conn.cursor(cursor_factory=extras.RealDictCursor)


def query_one(sql, **params):
    with closing(cursor()) as cur:
        cur.execute(sql, params)
        return cur.fetchone()


def query_all(sql, **params):
    with closing(cursor()) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def execute(sql, **params):
    with closing(cursor()) as cur:
        cur.execute(sql, params)


def commit():
    if hasattr(flask.g, DB_CONNECTION):
        conn = flask.g.dbconnection
        conn.commit()


def rollback():
    if hasattr(flask.g, DB_CONNECTION):
        conn = flask.g.dbconnection
        conn.rollback()


def transaction(func):
    @wraps(func)
    def inner(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as exception:
            rollback()
            logging.getLogger('sql').error("%s: %s" % (exception.__class__.__name__, exception))
        else:
            commit()
        finally:
            close()
        return result
    return inner


def call(filename):
    execute(open(os.path.join(app.config['SQL_FOLDER'], filename), mode='r').read())
    commit()


def create_all():
    with app.app_context():
        # Schema creating
        call('000_schema.sql')

        # Data adding
        call('001_add_data.sql')


def drop_all():
    with app.app_context():
        call('002_delete_data.sql')
        close()
