from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from database.database import db


user_identifier = db.Table('user_identifier', db.Model.metadata,
    db.Column('group_id', db.Integer, db.ForeignKey('Group.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('Student.id'))
)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship(
        'User', secondary=user_identifier
    )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    # internal user info
    registered_at = db.Column(
        db.DateTime, server_default=datetime.utcnow, nullable=False
    )
    last_login = db.Column(
        db.DateTime, nullable=True
    )

    def __init__(self, username, email, password=None):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

