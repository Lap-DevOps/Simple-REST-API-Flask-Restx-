import uuid
from datetime import datetime

import pytest
from flask import Flask

from app import create_app, db
from app.models.user import User
from app.models.post import Post
from app.models.like import Like


@pytest.fixture
def app(monkeypatch) -> Flask:
    """Provides an instance of our Flask app with a specific configuration."""

    monkeypatch.setenv("FLASK_ENV", 'testing')
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_sqlalchemy_database_uri(app):
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'


def test_user_model_basic(app):
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='test@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()

        # Retrieve the user from the database
        retrieved_user = User.query.filter_by(username='testuser').first()

        # Check that the user was successfully added and retrieved
        assert user.id is not None
        assert retrieved_user is not None
        assert retrieved_user.username == 'testuser'
        assert retrieved_user.email == 'test@example.com'
        assert retrieved_user.verify_password('testpassword')
        assert retrieved_user.password_hash is not None
        assert isinstance(retrieved_user.member_since, datetime)


def test_user_password_property(app):
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='test@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()

        try:
            password = user.password
        except AttributeError as e:
            assert str(e) == 'password is not a readable attribute'
        else:
            assert False, "Accessing the 'password' property did not raise the expected AttributeError"


def test_public_id(app):
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='test@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username='testuser').first()

        assert hasattr(retrieved_user, 'public_id'), "Model does not have 'public_id' attribute"

        # Check if 'public_id' is a string in UUID format
        try:
            uuid_obj = uuid.UUID(retrieved_user.public_id, version=4)
        except ValueError:
            assert False, "'public_id' is not a valid UUID"
        else:
            assert str(uuid_obj) == retrieved_user.public_id, "'public_id' is not a valid UUID string"


def test_user_verify_password(app):
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='test@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()

        # Check that the verify_password function works correctly
        assert user.verify_password('testpassword')
        assert not user.verify_password('wrongpassword')


def test_user_repr(app):
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='test@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()

        # Check that the __repr__ function returns the expected string
        expected_repr = f"<User :  {user.username}, email: {user.email}, ID: {user.id}>"
        assert repr(user) == expected_repr


def test_update_last_login(app):
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='test@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()

        # Retrieve the user from the database
        retrieved_user = User.query.filter_by(username='testuser').first()

        # Record the current time
        current_time = datetime.utcnow()

        # Update last_login
        retrieved_user.update_last_login()
        db.session.commit()

        # Retrieve the updated user
        updated_user = User.query.filter_by(username='testuser').first()

        # Check that last_login is set and is a datetime
        assert updated_user.last_login is not None
        assert isinstance(updated_user.last_login, datetime)

        # Check that last_login was updated within a reasonable range
        assert current_time <= updated_user.last_login <= datetime.utcnow()


def test_update_last_api_request(app):
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='test@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()

        # Retrieve the user from the database
        retrieved_user = User.query.filter_by(username='testuser').first()

        # Record the current time
        current_time = datetime.utcnow()

        # Update last_api_request
        retrieved_user.update_last_api_request()
        db.session.commit()

        # Retrieve the updated user
        updated_user = User.query.filter_by(username='testuser').first()

        # Check that last_api_request is set and is a datetime
        assert updated_user.last_api_request is not None
        assert isinstance(updated_user.last_api_request, datetime)

        # Check that last_api_request was updated within a reasonable range
        assert current_time <= updated_user.last_api_request <= datetime.utcnow()


if __name__ == "__main__":
    pytest.main()
