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


def test_post_model_basic(app):
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

        # Retrieve the post from the database
        retrieved_post = Post.query.filter_by(title="Test Post").first()

        assert post.id is not None
        assert retrieved_post is not None
        assert retrieved_post.title == "Test Post"
        assert retrieved_post.content == "This is a test post"
        assert retrieved_post.slug is not None
        assert isinstance(retrieved_post.date_posted, datetime)
        assert retrieved_post.author == user
        #
        # Additional check for slug generation
        assert post.slug == "test-post"
        #
        # # Additional check for the association with the author (user)
        assert len(user.posts) == 1
        assert post in user.posts


def test_post_generate_slug_no_title(app):
    with app.app_context():
        post = Post(title="", content="Test Content")
        assert post.generate_slug("") == None


@pytest.mark.parametrize(
    "title, expected_slug",
    [
        ("Hello World", "hello-world"),
        ("Lorem Ipsum", "lorem-ipsum"),
        ("123 Test 456", "123-test-456"),
        ("!@#$%^&*()_+", ""),
        ("Special Characters", "special-characters"),
    ],
)
def test_post_generate_slug(app, title, expected_slug):
    with app.app_context():
        user = User(
            username="testuser", email="test@example.com", password="testpassword"
        )
        db.session.add(user)
        db.session.commit()

        post = Post(title=title, content="Test Content", author=user)
        db.session.add(post)
        db.session.commit()

        assert post.slug == expected_slug


def test_post_repr(app):
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

        # Retrieve the post from the database
        retrieved_post = Post.query.filter_by(author_id=user.id).first()

        # Check that the __repr__ function returns the expected string
        expected_repr = f"Post(id={retrieved_post.id}, title={retrieved_post.title}, date_posted={retrieved_post.date_posted.strftime('%d.%m.%Y-%H.%M')}, author_id={retrieved_post.author_id})"
        assert repr(post) == expected_repr


def test_slug_change(app):
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

        retrieved_post = Post.query.filter_by(author_id=user.id).first()
        assert retrieved_post.title == "Test Post"
        assert post.slug == "test-post"

        retrieved_post.title = "New test post"
        db.session.add(retrieved_post)
        db.session.commit()

        new_retrieved_post = Post.query.filter_by(author_id=user.id).first()

        assert new_retrieved_post.title == "New test post"
        assert new_retrieved_post.slug == "new-test-post"


if __name__ == "__main__":
    pytest.main()
