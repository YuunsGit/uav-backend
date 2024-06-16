from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.join(path.dirname(__file__), '..'))
load_dotenv()


class BaseConfig(object):
    """ Base config class. """
    APP_NAME = environ.get('APP_NAME') or 'UAV-Monitoring'
    FLASK_APP = environ.get('FLASK_APP') or 'run.py'
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(BaseConfig):
    """ Development config. """
    DEBUG = True
    ENV = 'dev'


class Test(BaseConfig):
    """ Test config. """
    DEBUG = False
    ENV = 'test'


class Production(BaseConfig):
    """ Production config """
    DEBUG = False
    ENV = 'production'


config = {
    'development': Development,
    'test': Test,
    'production': Production,
}