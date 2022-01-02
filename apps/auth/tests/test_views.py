from flask import url_for
from flask_login import login_user

from apps.base.tests.test_base import (
    session, db, app, test_app, request_context, credentials, user
)
from apps.base.tests.test_utilities import login, logout


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
    pass


def test_post_register_not_authenticated_incorrect_data(test_app)
    pass


def test_post_register_authenticated(test_app, user):
    pass
