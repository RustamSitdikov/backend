#!/usr/bin/env python

import flask
import psycopg2
from psycopg2 import extras
from contextlib import closing
from functools import wraps
import logging
import os
from config import Config

DB_CONNECTION = "dbconnection"


def connection():
    if not hasattr(flask.g, DB_CONNECTION):
        flask.g.dbconnection = psycopg2.connect(
            database=Config.DATABASE_NAME,
            user=Config.DATABASE_USER, password=Config.DATABASE_PASSWORD,
            host=Config.DATABASE_HOST
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


def call_db(filename):
    execute(open(os.path.join(Config.SQL_FOLDER, filename), mode='r').read())
    commit()


def init_db():
    # Schema creating
    call_db('000_schema.sql')

    # Data adding
    call_db('001_add_data.sql')


def close_db():
    call_db('003_delete_data.sql')
    close()