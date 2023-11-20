import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
dotenv_path = os.path.join(parent_dir, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")
    SECURITY_PASSWORD_SALT = (
        os.environ.get("SECURITY_PASSWORD_SALT") or "hard to guess string"
    )
    SECURITY_PASSWORD_HASH = "sha512_crypt"
    DEBUG = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.environ.get('DEV_DATABASE_USER')}:"
        f"{os.environ.get('DEV_DATABASE_PASSWORD')}@{os.environ.get('DEV_DATABASE_HOST')}:"
        f"{os.environ.get('DEV_DATABASE_PORT')}/{os.environ.get('DEV_DATABASE_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    ENV = "testing"
    DEBUG = True
    TESTING = True
    RESTX_MASK_SWAGGER = True

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite:///:memory:"
    )
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.environ.get('PROD_DATABASE_USER')}:"
        f"{os.environ.get('PROD_DATABASE_PASSWORD')}@{os.environ.get('PROD_DATABASE_HOST')}:"
        f"{os.environ.get('PROD_DATABASE_PORT')}/{os.environ.get('PROD_DATABASE_NAME')}"
    )
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
