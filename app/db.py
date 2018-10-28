import flask
import psycopg2
import config

def get_connection():
    if not hasattr(flask.g, 'dbconn'):
        flask.g.dbconn = psycopg2.connect(database=config.DB_NAME, host=config.DB_HOST,
            user=config.DB_USER, password=config.DB_PASS)
        return flask.g.dbconn

def get_cursor():
    return get_connection().cursor(cursor_factory=psycopg2.extras.DictCursor)

def query_one(sql, **params):
    with get_cursor() as cursor:
        cursor.execute(sql, params)
        return dict(cursor.fetchone())

