import os


"""
In this module we will keep global application configuration, for example, 
DEBUG settings or database url, this will make managing such settings 
much easier. 
"""


class BasicConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", '57e19ea558d4967a552d03deece34a70'
    )


class ProductionConfig(BasicConfig):
    """
    Config to be used on production server
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG = False


class DevelopmentConfig(BasicConfig):
    """
    Config to be used on a private developer desktop
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    DEVELOPMENT = True
    DEBUG = True


class TestConfig(BasicConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

