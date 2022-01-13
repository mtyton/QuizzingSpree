from database.database import db


class QuizCategory(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(150))

    def __init__(self, category_name):
        self.category_name = category_name


class Quiz(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(150), db.ForeignKey('quizcategory.category_name')) 
    difficulty_level = db.Column(db.String(150))
    questions = db.relationship('Question', backref='quiz', lazy=True)

    def __init__(self, category, difficulty_level, questions):
        self.category = category
        self.difficulty_level = difficulty_level
        self.questions = questions


class Question(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    question_type = db.Column(db.String(150))

    def __init__(self, answer_id, question_type):
        self.answer_id = answer_id
        self.question_type = question_type


class Answer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    correct = db.Column(db.Boolean)

    def __init__(self, text, correct):
        self.text = text
        self.correct = correct
