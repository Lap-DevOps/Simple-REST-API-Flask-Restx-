import re
from datetime import datetime

from slugify import slugify
from sqlalchemy import DateTime
from sqlalchemy.orm import validates

from app import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False, index=True)
    content = db.Column(db.Text(), nullable=False)
    slug = db.Column(db.String(140), unique=True)
    date_posted = db.Column(
        DateTime(), nullable=False, default=datetime.now, index=True
    )

    author_id = db.Column(
        db.String(50), db.ForeignKey("users.public_id", ondelete="CASCADE"), nullable=False
    )
    likes = db.relationship(
        "Like", backref="post", lazy=True, cascade="all, delete-orphan"
    )

    @validates("title")
    def validate_title(self, key, title):
        self.generate_slug(title)
        return title

    def generate_slug(self, title):
        # pattern = r'[^\w+]'
        if title:
            # self.slug = re.sub(pattern, '-', title).lower()
            self.slug = slugify(title)

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, date_posted={self.date_posted.strftime('%d.%m.%Y-%H.%M')}, author_id={self.author_id})"
