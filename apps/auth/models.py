import sqlalchemy as sa

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    # internal user info
    registered_at = db.Column(
        db.DateTime, server_default=sa.text("CURDATE()"), nullable=False
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
