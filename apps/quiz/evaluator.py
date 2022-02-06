from flask_login import current_user

from database.database import db
from apps.quiz.models import UserQuizAttempt, Quiz, Question


class EvaluationUtils:

    @staticmethod
    def calculate_points(question: Question, number_of_correct: int) -> float:
        if not question.correct_answers.count():
            return 0.0
        return float(number_of_correct)/float(question.correct_answers.count())


class QuizEvaluator:

    @staticmethod
    def evaluate(quiz: Quiz, data: dict) -> UserQuizAttempt:
        score = 0

        for solution in data.get('questions', []):
            # make sure that we will retrieve question
            if not (question := solution.get('question')):
                continue
            # TODO - add question variable type verification
            # get all available answers for given question
            question_answers = question.answers
            number_of_correct = 0
            for answer_id in solution.get('answers'):
                current_answer = question_answers.filter_by(
                    id=int(answer_id)
                ).first()
                if current_answer.correct:
                    number_of_correct += 1
            score += EvaluationUtils.calculate_points(
                question, number_of_correct
            )

        attempt = UserQuizAttempt(quiz=quiz, user=current_user, score=score)
        db.session.add(attempt)
        db.session.commit()
        return attempt
