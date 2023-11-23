import pytest
from flask import Flask, current_app
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.models.user import User


@pytest.fixture
def app(monkeypatch) -> Flask:
    """Provides an instance of our Flask app with a specific configuration."""

    monkeypatch.setenv("FLASK_ENV", "testing")
    app = create_app()
    with app.app_context():
        assert current_app.config["TESTING"] is True
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def registered_user(app):
    # Create two users
    user1 = User(username="user1", email="user1@example.com")
    user2 = User(username="user2", email="user2@example.com")

    # Save them to the database
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Create tokens for the users
    token_user1 = create_access_token(identity=user1.public_id)
    token_user2 = create_access_token(identity=user2.public_id)

    # Return user data and tokens as a dictionary
    return {
        "user1": {"user": user1, "token": token_user1},
        "user2": {"user": user2, "token": token_user2},
    }


def test_get_user_status_code(client, registered_user):
    # Example using data from the first user
    user1_data = registered_user["user1"]
    response = client.get("/api/user/", headers={"Authorization": f"Bearer {user1_data['token']}"})

    assert response.status_code == 200


def test_get_empty_user_list(client, registered_user):
    """Test for accessing the /api/user/ endpoint with an empty database."""
    user1_data = registered_user["user1"]
    response = client.get("/api/user/", headers={"Authorization": f"Bearer {user1_data['token']}"})
    assert response.status_code == 200
    assert b'"total": 2' in response.data


def test_get_one_user(client, registered_user):
    """Test for accessing the /api/user/ endpoint with a database containing one user."""
    user1_data = registered_user["user1"]

    response = client.get("/api/user/", headers={"Authorization": f"Bearer {user1_data['token']}"})
    assert response.status_code == 200
    assert b'"total": 2' in response.data
    assert b'"data":' in response.data
    assert b'"id":' in response.data
    assert b'"username": "user1"' in response.data
    assert b'"email": "user1@example.com"' in response.data
    assert b'"member_since"' in response.data


def test_get_two_users(client, registered_user):
    """Test for accessing the /api/user/ endpoint with a database containing two users."""
    user2_data = registered_user["user2"]

    response = client.get("/api/user/", headers={"Authorization": f"Bearer {user2_data['token']}"})
    assert response.status_code == 200
    assert b'"total": 2' in response.data
    assert b'"data":' in response.data
    assert b'"id":' in response.data
    assert b'"username": "user1"' in response.data
    assert b'"email": "user1@example.com"' in response.data
    assert b'"username": "user2"' in response.data
    assert b'"email": "user2@example.com"' in response.data


def test_create_user(client):
    """Test for creating a user"""

    payload = {"username": "user", "email": "user@tast.com", "password": "password"}

    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 201
    assert "id" in response.json
    assert "username" in response.json
    assert "email" in response.json
    assert "member_since" in response.json


@pytest.mark.parametrize(
    "invalid_payload, expected_error",
    [
        (
            {"username": "", "email": "user@tast.com", "password": "password"},
            "Username must be at least 4 characters long",
        ),
        (
            {"username": "user", "email": "invalid_email", "password": "password"},
            "Invalid email format",
        ),
        (
            {"username": "user", "email": "user@tast.com", "password": "short"},
            "Password must be at least 8 characters long",
        ),
    ],
)
def test_create_user_validation_errors(client, invalid_payload, expected_error):
    """Test for creating a user with validation errors"""

    response = client.post("/api/auth/register", json=invalid_payload)

    assert response.status_code == 400
    assert "message" in response.json
    assert expected_error in response.json["message"]


if __name__ == "__main__":
    pytest.main()
