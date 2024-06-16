from flask import Flask
from os import environ
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from .config import config as app_config

db = SQLAlchemy()


def create_app():
    load_dotenv()
    app_env = environ.get('APPLICATION_ENV') or 'development'

    app = Flask(app_config[app_env].APP_NAME)
    app.config.from_object(app_config[app_env])

    from app.routes import register_routes
    register_routes(app, db)

    db.init_app(app)
    migrate = Migrate(app, db)

    return app
