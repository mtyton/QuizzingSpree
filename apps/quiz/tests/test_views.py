from flask import url_for

from apps.base.tests.test_base import (
    session, db, app, test_app, request_context, credentials, user
)
from apps.quiz.tests.fixtures import (
    quiz_obj, select_multiple_question_data,
    select_question_data, quiz_creation_data,
    quiz_request_data, category_obj
)
from apps.base.tests.test_utilities import login, logout
from apps.quiz.models import Quiz


# testing creator views

def test_post_create_quiz_view_success(db, test_app, quiz_request_data, user):
    login(test_app, user.username, "complexP@ssworD")
    data = quiz_request_data.copy()

    data['title'] = "FirstSuccessQuiz"
    response = test_app.post(
        url_for("quiz.quiz_create"),
        data=data
    )
    # check if Quiz has been created
    quiz = Quiz.query.filter_by(title="FirstSuccessQuiz").first()
    assert quiz is not None
    assert response.status_code == 302
    logout(test_app)


def test_post_create_quiz_view_missing_data(
        db, test_app, quiz_request_data, user, session
):
    # add user to session
    # FIXME
    session.add(user)

    login(test_app, user.username, "complexP@ssworD")
    data = quiz_request_data.copy()
    # pop necessary data keys
    data.pop('title')

    response = test_app.post(
        url_for("quiz.quiz_create"),
        data=data
    )
    assert response.status_code == 200
    logout(test_app)
    # TODO
    # assert b"" in response.data


def test_post_create_quiz_view_not_authenticated(
        db, test_app, quiz_request_data, user
):
    data = quiz_request_data.copy()
    data['title'] = "SecondSuccessQuiz"

    response = test_app.post(
        url_for("quiz.quiz_create"),
        data=data
    )
    # check if Quiz has been created
    quiz = Quiz.query.filter_by(title="SecondSuccessQuiz").first()
    assert quiz is None
    assert response.status_code == 301


# Testing solver views

def test_get_question_solver_not_authenticated(
    db, test_app, quiz_obj, user
):
    response = test_app.get(
        url_for('quiz.quiz_solve', **{'quiz_id': quiz_obj.id})
    )
    assert response.status_code == 301


def test_get_question_solver_authenticated(
    db, test_app, quiz_obj, user
):
    login(test_app, user.username, "complexP@ssworD")
    response = test_app.get(
        url_for('quiz.quiz_solve', **{'quiz_id': quiz_obj.id})
    )
    assert response.status_code == 200
    logout(test_app)

# TODO - write tests for post
