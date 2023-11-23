import random
from datetime import datetime, timedelta

import pytest
from flask import Flask, current_app
from flask_jwt_extended import create_access_token

from app import create_app
from app import db
from app.models.like import Like
from app.models.post import Post
from app.models.user import User


@pytest.fixture()
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


@pytest.fixture()
def users(app):
    users_data = [
        {"username": "user1", "email": "user1@example.com", "password": "password1"},
        {"username": "user2", "email": "user2@example.com", "password": "password2"},
        {"username": "user3", "email": "user3@example.com", "password": "password3"},
        {"username": "user4", "email": "user4@example.com", "password": "password4"},
        {"username": "user5", "email": "user5@example.com", "password": "password5"},
    ]
    users = []
    with app.app_context():
        for user_data in users_data:
            user = User(**user_data)
            db.session.add(user)
        db.session.commit()
        users.extend(User.query.all())
    return users


@pytest.fixture()
def posts(app, users):
    posts_data = []
    for user in users:
        for i in range(5):
            post_data = {
                "title": f"Post {i + 1} by {user.username}",
                "content": f"Content {i + 1} by {user.username}",
                "author_id": user.public_id,
            }
            posts_data.append(post_data)
    with app.app_context():
        posts = []
        for post_data in posts_data:
            post = Post(**post_data)
            db.session.add(post)
        db.session.commit()
        posts.extend(Post.query.all())
    return posts


@pytest.fixture()
def likes(app, users, posts):
    current_time = datetime.utcnow()
    likes = []
    for user in users:
        for post in posts:
            # Each user likes 20 posts by other users (excluding their own)
            if user.public_id != post.author_id:
                created_at = current_time - timedelta(days=random.randint(1, 10))  # random likes in 10 days
                like = Like(user_id=user.public_id, post_id=post.id, created_at=created_at)
                db.session.add(like)
    db.session.commit()


@pytest.fixture()
def client(app, users, posts, likes):
    client = app.test_client()
    user = User.query.get(1)
    client.jwt_token = create_access_token(identity=user.public_id, fresh=True)
    return client


def test_get_all_users_posts(app, client):
    # Create data using fixtures

    # Send a GET request to retrieve all users
    response_users = client.get("/api/user/", headers={"Authorization": f"Bearer {client.jwt_token}"})

    # Check that the response status code is 200 OK
    assert response_users.status_code == 200
    #
    # # Check that the response contains the expected number of users
    assert response_users.json["total"] == 5  # Assuming we have 5 users
    #
    # # Send a GET request to retrieve all posts
    response_posts = client.get("/api/post/", headers={"Authorization": f"Bearer {client.jwt_token}"})
    #
    # # Check that the response status code is 200 OK
    assert response_posts.status_code == 200
    #
    # # Check that the response contains the expected number of posts
    assert response_posts.json["total"] == 25  # Assuming we have 25 posts
    #
    # # Check that each post has 4 likes
    for like_number in range(1, 26):
        response_posts_likes = client.get(
            f"/api/post/{like_number}",
            headers={"Authorization": f"Bearer {client.jwt_token}"},
        )

        # # Check that the response status code is 200 OK
        assert response_posts_likes.status_code == 200


def test_post_likes(app, client):
    response_posts_likes = client.get(f"/api/post/1", headers={"Authorization": f"Bearer {client.jwt_token}"})
    post = Post.query.get(1)
    assert response_posts_likes.status_code == 200
    assert len(post.likes) == response_posts_likes.json["likes"]


def test_likes_analytics(client):
    # Send a GET request to retrieve all likes statistic
    response_posts_likes = client.get("/api/analytics/", headers={"Authorization": f"Bearer {client.jwt_token}"})

    # Check that the response status code is 200 OK
    assert response_posts_likes.status_code == 200
    assert response_posts_likes.json["total_likes"] == 100


def test_user_analytics(client, users):
    # Retrieve the first user from the database
    user = User.query.get(1)

    # Check that the user's last_login and last_api_request are initially None
    assert user.last_login is None
    assert user.last_api_request is None

    # Perform a login request to obtain an access token
    login_user = client.post("/api/auth/login", json={"email": "user1@example.com", "password": "password1"})
    user_token = login_user.json["access_token"]

    # Check that the login request returns a status code of 200 OK
    assert login_user.status_code == 200

    # Perform an API request on behalf of the user
    any_user_api_request = client.get("/api/user/", headers={"Authorization": f"Bearer {user_token}"})

    # Check that the API request returns a status code of 200 OK
    assert any_user_api_request.status_code == 200

    # Perform an analytics request to retrieve updated user data
    user_analytics_response = client.get("/api/analytics/user/1", headers={"Authorization": f"Bearer {user_token}"})
    user_new_data = user_analytics_response.json

    # Check that the analytics request returns a status code of 200 OK
    assert user_analytics_response.status_code == 200

    # Check that the "last login" and "last api request" fields are not None
    assert user_new_data["last login"] is not None
    assert user_new_data["last api request"] is not None

    # Check that the "last login" and "last api request" fields are instances of datetime
    assert isinstance(datetime.fromisoformat(user_new_data["last login"]), datetime)
    assert isinstance(datetime.fromisoformat(user_new_data["last api request"]), datetime)


if __name__ == "__main__":
    pytest.main()
