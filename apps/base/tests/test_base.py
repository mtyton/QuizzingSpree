"""
This module contains test base classes, and basic
test configuration. This file should be imported into
every other test file.
Classes which are here provide basic interface to interact with an application.
"""
import pytest

from app import create_app
from database.database import db as _db

from apps.auth.models import User


@pytest.fixture(scope='session')
def app():
    _app = create_app('config.TestConfig')
    yield _app


@pytest.fixture(scope='session')
def test_app(app):
    return app.test_client()


@pytest.fixture(scope="session")
def db(app):
    _db.app = app

    _db.init_app(app)
    _db.create_all(app=app)

    yield _db

    _db.drop_all()


@pytest.fixture(scope='session', autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()


@pytest.fixture
def request_context(app):
    """
       Creates the app and return the request context as a fixture
       so that this process does not need to be repeated in each test
    """
    return app.test_request_context


@pytest.fixture(scope='session', autouse=True)
def user(session):
    usr = User(
        username="testUser01", email="testUser1@test.com",
        password='complexP@ssworD'
    )
    session.add(usr)
    session.commit()
    return usr


@pytest.fixture
def credentials(user):
    return [('Authentication', user.get_id())]
