"""
This module contains test base classes, and basic
test configuration. This file should be imported into
every other test file.
Classes which are here provide basic interface to interact with an application.
"""
import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


class BaseTestCase:
    pass

