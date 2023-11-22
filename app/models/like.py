from datetime import datetime

from app import db


class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.String(50),
        db.ForeignKey("users.public_id", ondelete="CASCADE"),
        nullable=False,
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id'),)

    def __repr__(self):
        return f'<Like: user_id={self.user_id}, post_id={self.post_id}, created_at={self.created_at.strftime("%d.%m.%Y-%H.%M")}>'
