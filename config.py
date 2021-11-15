import os


"""
In this module we will keep global application configuration, for example, 
DEBUG settings or database url, this will make managing such settings 
much easier. 
"""


class BasicConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", '57e19ea558d4967a552d03deece34a70'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BasicConfig):
    """
    Config to be used on production server
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevelopmentConfig(BasicConfig):
    """
    Config to be used on a private developer desktop
    """
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True

# TODO - each one of you should create own config
# TODO - create some kind of config factory
