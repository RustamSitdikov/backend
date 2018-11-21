import os


class Config(object):
    DEBUG = False
    TESTING = False

    # Database
    DATABASE_NAME = "postgres"
    DATABASE_HOST = "127.0.0.1"
    DATABASE_PORT = "5432"
    DATABASE_USER = "postgres"
    DATABASE_PASSWORD = "6052940"

    # Session
    # SESSION_TYPE = 'redis'

    # S3
    S3_SERVICE_NAME = "S3"
    S3_BUCKET_NAME = "2018-sitdikov-rustam-bucket"
    S3_ENDPOINT_URL = "http://hb.bizmrg.com"
    S3_ACCESS_KEY_ID = "aajjK5UbPHYrTxo618EXLp"
    S3_SECRET_ACCESS_KEY = "d4SRR4d6HeL9MbxRxBAPQE78uwus5k2BFhSGr5FBLwWB"

    # Path
    SQL_FOLDER = os.path.join(os.getcwd(), 'sql')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'public')


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
