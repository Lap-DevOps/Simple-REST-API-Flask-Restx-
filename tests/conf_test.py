import os
import pytest
from app import create_app


def test_config_development(monkeypatch):
    """Test the configuration settings for the development environment."""
    # Set the environment to 'development'
    monkeypatch.setenv("FLASK_ENV", 'development')

    # Create the Flask app
    app = create_app()

    # Assertions for development environment configuration
    assert app.config["ENV"] == "development"
    assert app.config["DEBUG"] is True


def test_config_testing(monkeypatch):
    """Test the configuration settings for the testing environment."""
    # Set the environment to 'testing'
    monkeypatch.setenv("FLASK_ENV", 'testing')

    # Create the Flask app
    app = create_app()

    # Assertions for testing environment configuration
    assert app.config["ENV"] == "testing"
    assert app.config["DEBUG"] is True
    assert app.config["TESTING"] is True
    assert app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] is False
    assert app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'


def test_config_production(monkeypatch):
    """Test the configuration settings for the production environment."""
    # Set the environment to 'production'
    monkeypatch.setenv("FLASK_ENV", 'production')

    # Create the Flask app
    app = create_app()

    # Assertions for production environment configuration
    assert app.config["ENV"] == "production"
    assert app.config["DEBUG"] is False


if __name__ == "__main__":
    pytest.main()
