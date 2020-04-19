import os

from flask import Flask
import requests

base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", None)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(base_dir, "app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


def create_app(app_name=__name__, config_object=Config):
    app = Flask(
        app_name,
        template_folder="../../frontend/", static_folder="../../frontend"
    )
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    from apsaperudo.extensions import db, migrate, socketio
    db.init_app(app)
    migrate.init_app(app, db)
    # CORS is only allowed for dev purposes
    # Use FLASK_ENV?
    socketio.init_app(app, cors_allowed_origins='*')


app = create_app()

from apsaperudo.routes import *
from apsaperudo.sockets import *
from apsaperudo.database import models

if __name__ == '__main__':
    app.extensions["socketio"].run(app)
