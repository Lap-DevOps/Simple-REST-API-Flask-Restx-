import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import config

db = SQLAlchemy()
migrate = Migrate(db)


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

    # api = Api(app)


    return app
