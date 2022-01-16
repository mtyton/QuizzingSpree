from typing import List
from flask_login import current_user

from database.database import db

from apps.quiz import models as quiz_models
from apps.quiz import taxonomies as quiz_taxonomies
from apps.quiz.validators import DataEntriesRequiredValidator


# TODO - add sepparate ExceptionType for factories
class QuizFactory:

    question_factories: dict
    _errors: List[dict]

    REQUIRED_QUIZ_KEYS = [
        'title', 'author_id', 'category_id', 'description',
        'questions'
    ]

    def attach_factory(self, key, factory_class):
        self.question_factories[key] = factory_class()

    @property
    def errors(self):
        return self._errors

    def __init__(self):
        self._errors = []
        self.question_factories = {}

        # attach question factories
        self.attach_factory(
            quiz_taxonomies.QuestionTypeEnum.SELECT.value,
            SelectQuestionFactory
        )
        self.attach_factory(
            quiz_taxonomies.QuestionTypeEnum.SELECT_MULTIPLE.value,
            SelectMultipleQuestionFactory
        )

    def _validate_data(self, data: dict):
        self._errors = DataEntriesRequiredValidator.validate(
            self.REQUIRED_QUIZ_KEYS, data
        )
        if len(self._errors):
            return False
        return True

    def __create_question(
            self, quiz: quiz_models.Quiz, questions_data: List[dict]
    ) -> None:
        for question_kwargs in questions_data:
            factory = self.question_factories[
                question_kwargs.get('question_type')
            ]
            try:
                factory.create_question(quiz, question_kwargs)
            except AssertionError as e:
                self._errors += factory.get_errors()

    def create_quiz(self, data: dict) -> quiz_models.Quiz:
        if not self._validate_data(data):
            raise AssertionError(
                self.errors[0]['message']
            )

        questions_data = data.pop('questions')
        quiz = quiz_models.Quiz(**data)
        db.session.add(quiz)
        db.session.commit()

        self.__create_question(quiz, questions_data)

        if len(self.errors):
            raise AssertionError(
                self.errors[0]['message']
            )

        # commit database changes
        db.session.commit()
        return quiz


class BaseQuestionFactory:
    _errors: List[dict]
    REQUIRED_QUESTION_KEYS = [
        'question_type', 'content', 'answers'
    ]

    def __init__(self):
        self._errors = []

    def get_errors(self) -> List[dict]:
        return self._errors

    def _validate_data(self, data: dict) -> bool:
        self._errors = DataEntriesRequiredValidator.validate(
            self.REQUIRED_QUESTION_KEYS, data
        )
        if len(self._errors):
            return False

        return True

    def _cleaned_data(self, data: dict) -> dict:
        ...

    def _create_answers(
            self, question: quiz_models.Question, data: dict
    ) -> List[quiz_models.Answer]:
        answers = []
        for item in data.get('answers'):
            answer = quiz_models.Answer(question_id=question.id, **item)
            db.session.add(answer)
            answers.append(
                answer
            )
        return answers

    def create_question(
            self, quiz: quiz_models.Quiz, data: dict
    ) -> quiz_models.Question:
        if not self._validate_data(data):
            raise AssertionError(
                self.get_errors()[0]['message']
            )

        question = quiz_models.Question(
            quiz_id=quiz.id,
            **self._cleaned_data(data)
        )
        db.session.add(question)

        answers = self._create_answers(question, data)
        for answer in answers:
            question.answers.append(answer)

        return question


class SelectMultipleQuestionFactory(BaseQuestionFactory):

    def _validate_data(self, data: dict) -> bool:
        super()._validate_data(data)
        if not len(data.get('answers', [])) > 1:
            self._errors.append(
                {'message': "select_multiple can't have one answer!!"}
            )
            return False
        return True

    def _cleaned_data(self, data: dict) -> dict:
        return {
            'content': data['content'],
            'question_type': quiz_taxonomies.QuestionTypeEnum.SELECT_MULTIPLE
        }


class SelectQuestionFactory(BaseQuestionFactory):

    def _validate_data(self, data: dict) -> bool:
        super()._validate_data(data)
        if not len(data.get('answers', [])) > 0:
            self._errors.append(
                {'message': "select must have at least one answer!!"}
            )
            return False
        return True

    def _cleaned_data(self, data: dict) -> dict:
        return {
            'content': data['content'],
            'question_type': quiz_taxonomies.QuestionTypeEnum.SELECT
        }
