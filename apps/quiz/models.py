from database.database import db

from apps.quiz.taxonomies import (
    QuestionTypeEnum, QuizDifficultyLevelEnum
)


class QuizCategory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    slug_name = db.Column(db.String(50))
    category_name = db.Column(db.String(150))

    def __init__(self, category_name):
        self.category_name = category_name


class Quiz(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))

    category = db.Column(
        db.ForeignKey('quizcategory.id')
    )
    difficulty_level = db.Column(
        db.Enum(QuizDifficultyLevelEnum),
        default=QuizDifficultyLevelEnum.MEDIUM
    )

    description = db.Column(db.String(500))
    questions = db.relationship('Question', backref='quiz', lazy=True)

    def __init__(self, category, difficulty_level, questions):
        self.category = category
        self.difficulty_level = difficulty_level
        self.questions = questions


class Question(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250))

    question_type = db.Column(
        db.Enum(QuestionTypeEnum),
        default=QuestionTypeEnum.SELECT
    )
    answers = db.relationship('Answer', backref='question', lazy=True)

    def __init__(self, answer_id, question_type):
        self.answer_id = answer_id
        self.question_type = question_type


class Answer(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String(250))
    correct = db.Column(db.Boolean)

    def __init__(self, content: str, correct: bool):
        self.content = content
        self.correct = correct
