import os

from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from app.config import config
from app.resurses.post_resourse_v1 import post_namespace

db = SQLAlchemy()
migrate = Migrate(db)
bcrypt = Bcrypt()

api = Api(
    version="1.0",
    title="StarNavi API",
    description="A simple Post API",
)


def create_app() -> Flask:
    """
    Creates an application instance to run
    :return: A Flask object
    """
    #
    """Flask app factory

        :config_name: a string object.
        :returns: flask.Flask object

        """
    app = Flask(__name__)
    config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    api.init_app(app)
    api.add_namespace(post_namespace, path='/api/post')

    return app
