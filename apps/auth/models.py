import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from apps.quiz.models import UserQuizAttempt

from database.database import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    # internal user info
    registered_at = db.Column(
        db.DateTime, nullable=False
    )
    last_login = db.Column(
        db.DateTime, nullable=True
    )

    def __init__(self, username: str, email: str, password=None):
        self.username = username
        self.email = email
        self.set_password(password)
        # set initial registered_at - this has to be done here because SOMEHOW
        # mysql does not support CURDATE() during table creation, source:
        # https://stackoverflow.com/questions/20461030/current-date-curdate-not-working-as-default-date-value
        self.registered_at = datetime.date.today()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_latest_quiz_attempts(self, number_of_quizzes: int=10):
        this_user_attempts = UserQuizAttempt.query.filter_by(user_id=self.id).order_by(UserQuizAttempt.date.desc()).limit(number_of_quizzes).all()
        if this_user_attempts == []:
            return None
        else:
            return this_user_attempts
