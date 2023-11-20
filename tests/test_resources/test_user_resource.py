import pytest
from flask import Flask, current_app

from app import create_app, db
from app.models.like import Like
from app.models.post import Post
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


def test_get_user_status_code(client):
    # Предположим, что '/user' - это URL вашего ресурса для получения информации о пользователе
    response = client.get("/api/user/")

    assert response.status_code == 200


def test_get_empty_user_list(client):
    """Тест для обращения к эндпоинту /api/user/ с пустой базой данных."""
    response = client.get("/api/user/")
    assert response.status_code == 200
    assert b'"total": 0' in response.data
    assert b'"data": []' in response.data


def test_get_one_user(client):
    """Тест для обращения к эндпоинту /api/user/ с базой данных, содержащей одного пользователя."""
    # Создаем одного пользователя
    user = User(username="test_user", email="test@example.com")
    db.session.add(user)
    db.session.commit()

    response = client.get("/api/user/")
    assert response.status_code == 200
    assert b'"total": 1' in response.data
    assert b'"data":' in response.data
    assert b'"id":' in response.data
    assert b'"username": "test_user"' in response.data
    assert b'"email": "test@example.com"' in response.data
    assert b'"member_since"' in response.data


def test_get_two_users(client):
    """Тест для обращения к эндпоинту /api/user/ с базой данных, содержащей двух пользователей."""
    user1 = User(username="user1", email="user1@example.com")
    user2 = User(username="user2", email="user2@example.com")
    db.session.add_all([user1, user2])
    db.session.commit()

    response = client.get("/api/user/")
    assert response.status_code == 200
    assert b'"total": 2' in response.data
    assert b'"data":' in response.data
    assert b'"id":' in response.data
    assert b'"username": "user1"' in response.data
    assert b'"email": "user1@example.com"' in response.data
    assert b'"username": "user2"' in response.data
    assert b'"email": "user2@example.com"' in response.data


def test_create_user_and_get_resource(client):
    """Test json response"""
    user = User(username="test_user", email="test@example.com")
    db.session.add(user)
    db.session.commit()

    response = client.get("/api/user/")

    # Проверяем, что статус код равен 200
    assert response.status_code == 200

    # Проверяем формат JSON-ответа
    expected_json = {
        "total": 1,
        "data": [
            {
                "id": str(user.public_id),
                "username": user.username,
                "email": user.email,
                "member_since": user.member_since.isoformat(),
            }
        ],
    }

    # Проверяем, что JSON-ответ соответствует ожидаемому формату
    assert response.get_json() == expected_json


# TODO paginated tests


def test_create_user(client):
    """Test user creation"""

    payload = {"username": "user", "email": "user@tast.com", "password": "password"}

    response = client.post("/api/user/", json=payload)

    assert response.status_code == 201
    assert "id" in response.json
    assert "username" in response.json
    assert "email" in response.json
    assert "member_since" in response.json


@pytest.mark.parametrize("invalid_payload, expected_error", [
    ({"username": "", "email": "user@tast.com", "password": "password"}, "Username must be at least 4 characters long"),
    ({"username": "user", "email": "invalid_email", "password": "password"}, "Invalid email format"),
    ({"username": "user", "email": "user@tast.com", "password": "short"}, "Password must be at least 8 characters long"),
])
def test_create_user_validation_errors(client, invalid_payload, expected_error):
    """Test user creation with validation errors"""

    response = client.post("/api/user/", json=invalid_payload)

    assert response.status_code == 400
    assert "message" in response.json
    assert expected_error in response.json["message"]



if __name__ == "__main__":
    pytest.main()
