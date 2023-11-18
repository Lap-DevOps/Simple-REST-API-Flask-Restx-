import os
import pytest
from flask import current_app, Flask
from app import create_app, db


@pytest.fixture
def app(monkeypatch) -> Flask:
    """Provides an instance of our Flask app with a specific configuration."""

    # Set the environment to 'testing'
    monkeypatch.setenv("FLASK_ENV", 'testing')

    # Create the Flask app
    app = create_app()

    return app


def test_app_exists(app):
    """Test if the Flask app instance exists."""
    assert current_app is not None


def test_config_testing(app):
    """Test if the app configuration is set to 'testing'."""
    assert app.config["ENV"] == "testing"


def test_app_settings(app):
    """Test specific settings of the Flask app."""
    assert app.config['DEBUG'] is True
    assert app.config['TESTING'] is True


def test_sqlalchemy_database_uri(app):
    """Test the SQLAlchemy database URI in the app configuration."""
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'


def test_example(app):
    """Example test using the Flask app."""
    # Your test using the app
    response = app.test_client().get('/')
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()
