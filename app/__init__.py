from flask import Flask
from os import environ
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from minio import Minio
from .config import config as app_config


MINIO_API_HOST = environ.get("MINIO_ENDPOINT")
ACCESS_KEY = environ.get("MINIO_ROOT_USER")
SECRET_KEY = environ.get("MINIO_ROOT_PASSWORD")

db = SQLAlchemy()
minio_client = Minio(MINIO_API_HOST, ACCESS_KEY, SECRET_KEY, secure=False)


def create_app():
    load_dotenv()
    app_env = environ.get('APPLICATION_ENV') or 'dev'

    app = Flask(app_config[app_env].APP_NAME)
    app.config.from_object(app_config[app_env])

    from app.routes import core as core_blueprint
    app.register_blueprint(
        core_blueprint,
        url_prefix='/api'
    )

    db.init_app(app)
    migrate = Migrate(app, db)

    return app
