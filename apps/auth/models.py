import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from apps.quiz.models import UserQuizAttempts, Quiz

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

    def get_last_10_quiz_attempts(self):
        this_user_attempts = UserQuizAttempts.query.filter_by(user_id=self.id).order_by(UserQuizAttempts.date.desc()).limit(10).all()
        if this_user_attempts == []:
            return "You don't have any quiz attempts yet"
        else:
            final_table = []
            for i in range (0, len(this_user_attempts)):
                quiz_name = Quiz.query.get(this_user_attempts[i].quiz_id).title
                score = this_user_attempts[i].score
                date = this_user_attempts[i].date.strftime("%m/%d/%Y, %H:%M:%S")
                final_table.append((quiz_name, score, date))
            return final_table
