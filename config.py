import os


class Config(object):
    DEBUG = False
    TESTING = False

    DATABASE_NAME = "postgres"
    DATABASE_HOST = "127.0.0.1"
    DATABASE_USER = "postgres"
    DATABASE_PASSWORD = "6052940"

    # SESSION_TYPE = 'redis'

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'public')

    # S3
    S3_SERVICE_NAME = "S3"
    S3_ENDPOINT_URL = "http://hb.bizmrg.com"
    S3_ACCESS_KEY_ID = None
    S3_SECRET_ACCESS_KEY = None

    S3_BUCKET_NAME = None


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
