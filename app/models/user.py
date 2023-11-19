import uuid
from datetime import datetime

from app import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, default=str(uuid.uuid4()), nullable=False, index=True)
    username = db.Column(db.String(120), unique=True, nullable=True)
    email = db.Column(db.String(120, collation='NOCASE'), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow())
    last_login = db.Column(db.DateTime(), nullable=True)
    last_api_request = db.Column(db.DateTime(), nullable=True)

    posts = db.relationship('Post',
                            backref='author',
                            lazy=True,
                            cascade='all, delete-orphan')
    likes = db.relationship('Like',
                            backref='author',
                            lazy=True)

    def update_last_login(self):
        self.last_login = datetime.utcnow()

    def update_last_api_request(self):
        self.last_api_request = datetime.utcnow()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User :  {self.username}, email: {self.email}, ID: {self.id}>'
