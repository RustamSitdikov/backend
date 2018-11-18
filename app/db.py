import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from config import Config


@contextmanager
def get_connection():
    connection = psycopg2.connect(
        database=Config.DATABASE_NAME, host=Config.DATABASE_HOST,
        user=Config.DATABASE_USER, password=Config.DATABASE_PASSWORD
    )
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        pass
        # connection.close()


def get_cursor():
    with get_connection() as connection:
        return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def query_one(sql, **params):
    with get_cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchone()


def query_all(sql, **params):
    with get_cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()
