import pytest
from flask import Flask
from sqlalchemy.exc import IntegrityError

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


def test_like_relationships(app):
    with app.app_context():
        # Создаем тестового пользователя
        user = User(username="testuser", email="test@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()

        # Создаем тестовый пост
        post = Post(title="Test Post", content="This is a test post", author=user)
        db.session.add(post)
        db.session.commit()

        # Создаем тестовый лайк
        like = Like(user_id=user.public_id, post_id=post.id)
        db.session.add(like)
        db.session.commit()

        # Получаем лайк из базы данных
        retrieved_like = Like.query.filter_by(user_id=user.public_id).first()

        # Проверяем связи между таблицами
        assert retrieved_like is not None
        assert retrieved_like.user_id == user.public_id
        assert retrieved_like.post_id == post.id


def test_user_post_like_relationships(app):
    with app.app_context():
        # Create a test user
        user = User(username="testuser", email="test@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()

        # Check that the user has no posts initially
        assert len(user.posts) == 0

        # Create a post for the user
        post = Post(title="Test Post", content="This is a test post", author=user)
        db.session.add(post)
        db.session.commit()

        # Check that the user now has this post
        assert user.posts == [post]

        # Check that the post has no likes initially
        assert len(post.likes) == 0

        # Create a like for the post
        like = Like(user_id=user.public_id, post_id=post.id)
        db.session.add(like)
        db.session.commit()

        # Check that the post now has the like
        assert post.likes == [like]

        # Check that the user now has the like
        assert user.likes == [like]

        # Check that the like now has the user and post
        assert like.user_id == user.public_id
        assert like.post_id == post.id
        assert isinstance(like.user_id, str)
        assert isinstance(like.post_id, int)


def test_user_multiple_posts(app):
    with app.app_context():
        # Create a test user
        user = User(username="testuser", email="test@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()

        # Check that the user has no posts initially
        assert len(user.posts) == 0

        # Create two posts for the user
        post1 = Post(title="Test Post 1", content="This is the first test post", author=user)
        post2 = Post(title="Test Post 2", content="This is the second test post", author=user)
        db.session.add_all([post1, post2])
        db.session.commit()

        # Check that the user now has two posts
        assert len(user.posts) == 2

        # Check that both posts are present for the user
        assert user.posts == [post1, post2]
        assert post1 in user.posts
        assert post2 in user.posts

        # Check that each post has a reference to the user
        assert post1.author == user
        assert post2.author == user


def test_user_has_multiple_posts_and_likes(app):
    with app.app_context():
        # Create a test user
        user = User(username="testuser", email="test@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()

        # Check that the user has no posts initially
        assert len(user.posts) == 0
        assert len(user.likes) == 0

        # Create two posts for the user
        post1 = Post(title="Test Post 1", content="This is the first test post", author=user)
        post2 = Post(title="Test Post 2", content="This is the second test post", author=user)
        db.session.add_all([post1, post2])
        db.session.commit()

        # Check that the user now has two posts
        assert len(user.posts) == 2

        # Check that both posts are present for the user
        assert user.posts == [post1, post2]

        # Check that each post has a reference to the user
        assert post1.author == user
        assert post2.author == user

        # Check that there are no likes initially
        assert Like.query.count() == 0

        # Create two likes for the posts
        like1 = Like(user_id=user.public_id, post_id=post1.id)
        like2 = Like(user_id=user.public_id, post_id=post2.id)
        db.session.add_all([like1, like2])
        db.session.commit()

        # Check that each post now has one like
        assert len(post1.likes) == 1
        assert len(post2.likes) == 1
        #
        # # Check that the user now has two likes
        assert len(user.likes) == 2
        #
        # # Check that both likes are present for the user
        assert user.likes == [like1, like2]
        assert like1 in user.likes
        assert like2 in user.likes

        # # Check that each like has a reference to the user and post
        assert like1.user_id == user.public_id
        assert like1.post_id == post1.id
        #
        assert like2.user_id == user.public_id
        assert like2.post_id == post2.id


def test_post_backref_to_user(app):
    with app.app_context():
        # Create a test user
        user = User(username="testuser", email="test@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()

        # Create a post for the user
        post = Post(title="Test Post", content="This is a test post", author=user)
        db.session.add(post)
        db.session.commit()

        # Check the backref from post to user
        assert post.author == user
        assert post.author_id == user.public_id
        assert len(user.posts) == 1
        assert user.posts[0] == post


def test_like_backref(app):
    with app.app_context():
        # Create a test user
        user = User(username="testuser", email="test@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()

        # Create a post for the user
        post = Post(title="Test Post", content="This is a test post", author=user)
        db.session.add(post)
        db.session.commit()

        # Create a like for the post
        like = Like(user_id=user.public_id, post_id=post.id)
        db.session.add(like)
        db.session.commit()

        # Check the back reference from the like to the user
        assert like.author == user
        assert like.user_id == user.public_id

        # Check the back reference from the like to the post
        assert like.post == post
        assert like.post_id == post.id


def test_delete_user_and_related_post(app):
    with app.app_context():
        # Create a test user
        user = User(username="testuser", email="test@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()

        # Create a post for the user
        post = Post(title="Test Post", content="This is a test post", author=user)
        db.session.add(post)
        db.session.commit()

        # Check that user and post exist in the database
        assert User.query.count() == 1
        assert Post.query.count() == 1

        # Delete the user (cascading delete should remove the related post)
        db.session.delete(user)
        db.session.commit()

        # Check that the user is removed from the database
        assert User.query.count() == 0

        # Check that the post is automatically deleted with the user
        assert Post.query.count() == 0


def test_delete_post_and_related_like(app):
    with app.app_context():
        # Create a test user
        user = User(username="testuser", email="test@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()

        # Create a post for the user
        post = Post(title="Test Post", content="This is a test post", author=user)
        db.session.add(post)
        db.session.commit()

        # Create a like for the post
        like = Like(user_id=user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()

        # Check that user, post, and like exist in the database
        assert User.query.count() == 1
        assert Post.query.count() == 1
        assert Like.query.count() == 1

        # Delete the post (cascading delete should remove the related like)
        db.session.delete(post)
        db.session.commit()

        # Check that the post is removed from the database
        assert Post.query.count() == 0

        # Check that the like is automatically removed
        assert Like.query.count() == 0


def test_delete_user_and_related_post_and_like(app):
    with app.app_context():
        # Create a test user
        user = User(username="testuser", email="test@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()

        # Create a post for the user
        post = Post(title="Test Post", content="This is a test post", author=user)
        db.session.add(post)
        db.session.commit()

        # Create a like for the post
        like = Like(user_id=user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()

        # Check that user, post, and like exist in the database
        assert User.query.count() == 1
        assert Post.query.count() == 1
        assert Like.query.count() == 1

        # Delete the user (cascading delete should remove related post and like)
        db.session.delete(user)
        db.session.commit()

        # Check that the user is removed from the database
        assert User.query.count() == 0

        # Check that the post and like are automatically removed
        assert Post.query.count() == 0
        assert Like.query.count() == 0


def test_user_cannot_like_post_twice(app):
    with app.app_context():
        # Create a test user
        user = User(username="testuser", email="test@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()

        # Create a post for the user
        post = Post(title="Test Post", content="This is a test post", author=user)
        db.session.add(post)
        db.session.commit()

        # Create a like for the post from the user
        like = Like(user_id=user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()

        # Attempt to create a second like from the same user for the same post
        with pytest.raises(IntegrityError):
            db.session.add(Like(user_id=user.id, post_id=post.id))
            db.session.commit()


if __name__ == "__main__":
    pytest.main()
