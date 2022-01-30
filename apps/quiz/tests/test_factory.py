from apps.base.tests.test_base import (
    session, db, app, test_app, request_context, credentials, user
)
from apps.quiz.tests.fixtures import (
    quiz_obj, select_multiple_question_data,
    select_question_data, quiz_creation_data,
    category_obj
)
from apps.quiz.quiz_factory import (
    SelectQuestionFactory, SelectMultipleQuestionFactory, QuizFactory
)
from apps.quiz.taxonomies import QuizDifficultyLevelEnum, QuestionTypeEnum


# Testing QuestionFactories
def test_select_multiple_question_correct_data(
        db, select_multiple_question_data, quiz_obj
):
    factory = SelectMultipleQuestionFactory()
    data = select_multiple_question_data.copy()
    question = factory.create_question(quiz_obj, data)
    assert question.question_type is QuestionTypeEnum.SELECT_MULTIPLE
    assert question.content == "Who is responsible for this?"


def test_select_multiple_question_invalid_data(
        db, select_multiple_question_data, quiz_obj
):
    factory = SelectMultipleQuestionFactory()
    # first make data invalid
    data = select_multiple_question_data.copy()

    data['answers'] = [{
        'content': 'Society',
        'correct': True
    }]
    try:
        factory.create_question(quiz_obj, data)
    except AssertionError as e:
        assert e.args[0] == "select_multiple can't have one answer!!"


def test_select_question_correct_data(
        db, select_question_data, quiz_obj
):
    factory = SelectQuestionFactory()
    data = select_question_data.copy()
    question = factory.create_question(quiz_obj, data)
    assert question.question_type is QuestionTypeEnum.SELECT
    assert question.content == "How much money does he has?"


def test_select_question_invalid_data(
        db, select_question_data, quiz_obj
):
    factory = SelectQuestionFactory()
    data = select_question_data.copy()
    data['answers'] = []

    try:
        factory.create_question(quiz_obj, data)
    except AssertionError as e:
        assert e.args[0] == "missing data for key: answers"


# Testing QuizFactory
def test_quiz_factory_complete_data_success(quiz_creation_data, db):
    factory = QuizFactory()
    quiz = factory.create_quiz(quiz_creation_data)
    assert quiz.title == "TEstQuiz"
    # TODO assert number of questions


def test_quiz_factory_missing_data(quiz_creation_data, db):
    factory = QuizFactory()
    quiz_creation_data.pop('title')
    try:
        factory.create_quiz(quiz_creation_data)
    except AssertionError as e:
        assert e.args[0] == "missing data for key: title"
