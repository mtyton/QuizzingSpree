from database.database import db


class Quiz(db.Model):

    __tablename__ = 'quiz'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(150), ) 
    difficulty_level = db.Column(db.String(150))
    questions = db.relationship('Question', backref='quiz', lazy=True)

    def __init__(self, category, difficulty_level, questions):
        self.category = category
        self.difficulty_level = difficulty_level


class QuizCategory(db.Model):

    __tablename__ = 'quiz_category'

    id = db.Column(db.Integer, primary_key=True)


class Question(db.Model):

    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), db.ForeignKey('answer.text'))
    question_type = db.Column(db.String(150))

    def __init__(self, category, difficulty_level):
        self.category = category
        self.difficulty_level = difficulty_level


class Answer(db.Model):

    __tablename__ = 'answer'

    text = db.Column(db.String(500))
    correct = db.Column(db.Boolean)
