import os

import pytest

from app import create_app


def test_config_development(monkeypatch):
    monkeypatch.setenv("FLASK_ENV", 'development')
    app = create_app()

    assert app.config["ENV"] == "development"
    assert app.config["DEBUG"] is True

def test_config_testing(monkeypatch):
    monkeypatch.setenv("FLASK_ENV", 'testing')
    app = create_app()

    assert app.config["ENV"] == "testing"
    assert app.config["DEBUG"] is True
    assert app.config["TESTING"] is True
    assert app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] is False
    assert app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'

def test_config_production(monkeypatch):
    monkeypatch.setenv("FLASK_ENV", 'production')
    app = create_app()
    assert app.config["ENV"] == "production"
    assert app.config["DEBUG"] is False

if __name__ == "__main__":
    pytest.main()




# @pytest.fixture
# def app() -> Flask:
#     """ Provides an instance of our Flask app """
#     from app import create_app
#
#     return create_app()
