import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = "lsk5jor7z3kL9£%jso1mq"

    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    pass