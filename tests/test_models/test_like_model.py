from datetime import datetime

import pytest
from flask import Flask

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
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_sqlalchemy_database_uri(app):
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_like_model_basic(app):
    with app.app_context():
        # Create a test user
        user = User(
            username="testuser", email="test@example.com", password="testpassword"
        )
        db.session.add(user)
        db.session.commit()

        # Create a test post
        post = Post(title="Test Post", content="This is a test post", author=user)
        db.session.add(post)
        db.session.commit()

        like = Like(user_id=user.public_id, post_id=post.id)
        db.session.add(like)
        db.session.commit()

        # Retrieve the post from the database
        retrieved_like = Like.query.filter_by(user_id=user.public_id).first()

        assert like.id is not None
        assert retrieved_like.id is not None
        assert retrieved_like is not None
        assert retrieved_like is not None
        assert retrieved_like.user_id == user.public_id
        assert retrieved_like.post_id == post.id
        assert isinstance(retrieved_like.created_at, datetime)
        assert retrieved_like.created_at <= datetime.utcnow()


def test_like_repr(app):
    with app.app_context():
        # Create test user
        user = User(
            username="testuser", email="test@example.com", password="testpassword"
        )
        db.session.add(user)
        db.session.commit()

        # Create test post
        post = Post(title="Test Post", content="This is a test post", author=user)
        db.session.add(post)
        db.session.commit()

        # Create a test like
        like = Like(user_id=user.id, post_id=post.id, created_at=datetime.utcnow())
        db.session.add(like)
        db.session.commit()

        # Check that the __repr__ function returns the expected string
        expected_repr = f"<Like: user_id={user.id}, post_id={post.id}, created_at={like.created_at.strftime('%d.%m.%Y-%H.%M')}>"
        assert repr(like) == expected_repr


if __name__ == "__main__":
    pytest.main()
