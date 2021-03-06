import datetime

from database.database import db
from apps.quiz.taxonomies import (
    QuestionTypeEnum, QuizDifficultyLevelEnum
)


class QuizCategory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    slug_name = db.Column(db.String(50))
    category_name = db.Column(db.String(150))

    def __init__(self, category_name, slug_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_name = category_name
        self.slug_name = slug_name

    def __str__(self):
        return self.category_name


class Quiz(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(
        db.Integer,  db.ForeignKey('quiz_category.id')
    )
    difficulty_level = db.Column(
        db.Enum(QuizDifficultyLevelEnum),
        default=QuizDifficultyLevelEnum.MEDIUM
    )

    description = db.Column(db.String(500))
    questions = db.relationship('Question', backref='quiz', lazy=True)
    author = db.relationship('User')

    def __init__(
            self, author_id: int, title: str, category_id: int,
            description: str, difficulty_level: QuizDifficultyLevelEnum = None,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.author_id = author_id
        self.category_id = category_id
        self.description = description
        self.title = title
        # if difficulty level has not been passed, use field default
        if not difficulty_level:
            self.difficulty_level = difficulty_level


class Question(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250))

    question_type = db.Column(
        db.Enum(QuestionTypeEnum),
        default=QuestionTypeEnum.SELECT
    )
    quiz_id = db.Column(
        db.Integer, db.ForeignKey('quiz.id'),
        nullable=False
    )

    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(
            self, content: str, question_type: QuestionTypeEnum,
            quiz_id: int, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.content = content
        self.question_type = question_type
        self.quiz_id = quiz_id

    @property
    def correct_answers(self):
        return self.answers.filter_by(correct=1)


class Answer(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String(250))
    correct = db.Column(db.Boolean)

    question_id = db.Column(
        db.Integer, db.ForeignKey('question.id'),
        nullable=False
    )

    def __init__(
            self, content: str, correct: bool,
            question_id: int, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.content = content
        self.correct = correct
        self.question_id = question_id


class UserQuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'),
        nullable=False
    )
    user = db.relationship(
        'User', backref=db.backref('quiz_attempts', lazy=True)
    )

    quiz_id = db.Column(
        db.Integer, db.ForeignKey('quiz.id'),
        nullable=False
    )
    quiz = db.relationship(
        'Quiz', backref=db.backref('users_attempts', lazy=True)
    )

    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(
            self, user, quiz: Quiz, score: int,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.user = user
        self.quiz = quiz
        self.score = score
        self.date = datetime.date.today()
