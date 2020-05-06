from price_scraper import database_uri


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "mysecret"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'test.flask369@gmail.com'
    MAIL_PASSWORD = 'Testflask369'

    MAIL_DEFAULT_SENDER = 'test.flask369@gmail.com'


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

