import pytest

from apps.base.tests.test_utilities import login
from apps.auth import models as user_models
from apps.quiz import models as quiz_models
from apps.quiz.taxonomies import QuizDifficultyLevelEnum


@pytest.fixture(scope='session')
def quiz_obj(db, test_app, user):
    category = quiz_models.QuizCategory(
        category_name="testCategory",
        slug_name="test_category"
    )
    db.session.add(category)
    db.session.commit()

    quiz = quiz_models.Quiz(
        author_id=user.id, category_id=category.id, description="TestDesc",
        title="TestQuiz"
    )
    db.session.add(quiz)
    db.session.commit()
    return quiz


@pytest.fixture(scope='session')
def select_multiple_question_data():
    return {
        'question_type': "select_multiple",
        'content': 'Who is responsible for this?',
        'answers': [{
            'content': 'Society',
            'correct': True
        }, {
            'content': 'MeMyselfAndI',
            'correct': True
        }, {
            'content': 'SomeFolk',
            'correct': False
        }, {
            'content': 'SomeOtherFolk',
            'correct': True
        }]
    }


@pytest.fixture(scope="session")
def select_question_data():
    return {
        'question_type': "select",
        'content': "How much money does he has?",
        'answers': [{
            'content': 'None',
            'correct': True
        }, {
            'content': '25 billions of dollars',
            'correct': False
        }, {
            'content': '25 cents',
            'correct': False
        }, {
            'content': 'No idea',
            'correct': False
        }]
    }


@pytest.fixture(scope="session")
def quiz_creation_data(
        test_app, user, db,
        select_question_data, select_multiple_question_data
):
    category = quiz_models.QuizCategory(
        category_name="testCategory",
        slug_name="test_category"
    )
    db.session.add(category)
    db.session.commit()

    db.session.add(user)
    return {
        'title': "TEstQuiz",
        'author_id': user.id,
        'category_id': category.id,
        'description': "TestDEscription",
        'questions': [
            select_question_data.copy(), select_multiple_question_data.copy(),
            select_question_data.copy(), select_multiple_question_data.copy(),
        ]
    }

