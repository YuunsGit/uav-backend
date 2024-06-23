from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.join(path.dirname(__file__), '..'))
load_dotenv()


class BaseConfig(object):
    """ Base configuration. """
    APP_NAME = environ.get('APP_NAME') or 'UAV-Monitoring'
    FLASK_APP = environ.get('FLASK_APP') or 'run.py'
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONIFY_PRETTYPRINT_REGULAR = True


class Development(BaseConfig):
    """ Development configuration. """
    DEBUG = True
    FLASK_DEBUG = 1
    ENV = 'dev'


class Test(BaseConfig):
    """ Testing configuration. """
    DEBUG = False
    TESTING = True
    ENV = 'test'


class Production(BaseConfig):
    """ Production configuration. """
    DEBUG = False
    ENV = 'prod'


config = {
    'dev': Development,
    'test': Test,
    'prod': Production,
}
