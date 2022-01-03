from flask import url_for
from flask_login import login_user

from apps.base.tests.test_base import (
    session, db, app, test_app, request_context, credentials, user
)
from apps.base.tests.test_utilities import login, logout
from apps.auth.models import User


def test_get_register_view_as_authenticated(test_app, user):
    login(test_app, user.username, "complexP@ssworD")
    response = test_app.get(url_for('auth.register'))
    assert response.status_code == 302


def test_get_register_view_as_not_authenticated(test_app):
    response = test_app.get(url_for('auth.register'))
    assert response.status_code == 200


def test_get_register_view_after_logout(test_app, user):
    login(test_app, user.username, "complexP@ssworD")
    response = test_app.get(url_for('auth.register'))
    assert response.status_code == 302
    # then logout and check if can access
    logout(test_app)
    response = test_app.get(url_for('auth.register'))
    assert response.status_code == 200


def test_post_register_not_authenticated_success(test_app):
    register_form_data = {
        'username': "testUser",
        'email': "test@mtyton.com",
        'password': "complexTestP@ssw0rD",
        'confirm': "complexTestP@ssw0rD",
        'accept_tos': True
    }
    response = test_app.post(url_for('auth.register'), data=register_form_data)

    assert response.status_code == 201
    user = User.query.filter_by(username=register_form_data['username']).first()
    assert user is not None


def test_post_register_not_authenticated_incorrect_data(test_app):
    register_form_data = {
        'username': "testUser",
        'email': "test@mtyton.com",
        'password': "complexTestP@ssw0rD",
        'confirm': "differentPassword",
        'accept_tos': True
    }
    response = test_app.post(url_for('auth.register'), data=register_form_data)

    assert response.status_code == 200
    user = User.query.filter_by(username=register_form_data['username']).first()
    assert user is None


def test_post_register_authenticated(test_app, user):
    login(test_app, user.username, "complexP@ssworD")

    register_form_data = {
        'username': "testUser",
        'email': "test@mtyton.com",
        'password': "complexTestP@ssw0rD",
        'confirm': "complexTestP@ssw0rD",
        'accept_tos': True
    }
    response = test_app.post(url_for('auth.register'), data=register_form_data)

    assert response.status_code == 302
    user = User.query.filter_by(username=register_form_data['username']).first()
    assert user is None


def test_get_login_not_authenticated(test_app):
    response = test_app.get(url_for('auth.login'))
    assert response.status_code == 200


def test_get_login_authenticated(test_app, user):
    login(test_app, user.username, "complexP@ssworD")

    response = test_app.get(url_for('auth.login'))
    assert response.status_code == 302


def test_post_login_not_authenticated_success(test_app):
    pass


def test_post_login_not_authenticated_wrong_password(test_app):
    pass


def test_post_login_authenticated(test_app, user):
    login_data = {
        'username': user.username,
        'password': "complexP@ssworD"
    }
