import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from app.config import config
from app.extensions import authorizations

db = SQLAlchemy()
migrate = Migrate(db)
bcrypt = Bcrypt()
jwt = JWTManager()

api = Api(
    version="1.0",
    title="StarNavi API",
    description="A simple Post API",
    authorizations=authorizations
    # doc='/swagger'
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
    config_name = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.models import like, post, user

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    api.init_app(app, validate=True)
    jwt.init_app(app)

    from app.resurses.user_resourse_v1 import user_namespace
    from app.resurses.post_resourse_v1 import post_namespace
    from app.resurses.like_resourse_v1 import like_namespace
    from app.auth.auth_resourse_v1 import auth_namespace

    api.add_namespace(auth_namespace, path="/api/auth")
    api.add_namespace(user_namespace, path="/api/user")
    api.add_namespace(post_namespace, path="/api/post")
    api.add_namespace(like_namespace, path="/api/post")

    return app
