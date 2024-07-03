from os.path import abspath, dirname, join

basedir = abspath(dirname(__file__))


class Config:
    SECRET_KEY = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'thermos.db')
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False
    SERVER_NAME = "localhost"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'thermos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
