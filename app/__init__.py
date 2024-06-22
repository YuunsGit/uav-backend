from flask import Flask
from os import environ
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from .config import config as app_config
from flask_cors import CORS


db = SQLAlchemy()
load_dotenv()


def create_app():
    app_env = environ.get('APPLICATION_ENV') or 'dev'

    app = Flask(app_config[app_env].APP_NAME)
    app.config.from_object(app_config[app_env])
    CORS(app)

    from app.routes import core as core_blueprint
    app.register_blueprint(
        core_blueprint,
        url_prefix='/app/api'
    )

    db.init_app(app)
    migrate = Migrate(app, db)

    return app
