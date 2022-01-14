import os

from flask import Flask

from database import database
from apps.auth.login_manager import configure_login_manager
from apps.auth.views import bp as bp_auth
from apps.website.views import bp as bp_web
from apps.quiz.views import bp as bp_quiz
from apps.base.context_processor import logged_user

# TODO - find better way (using flask-migrate)
# import models to allow creation during startup
from apps.auth import models as user_models
from apps.quiz import models as quiz_models


def get_proper_config_name(mode):
    if mode == "development":
        return 'config.DevelopmentConfig'
    return 'config.ProductionConfig'


def __configure_context_processors(app) -> Flask:
    app.context_processor(logged_user)
    return app


def create_app(predefined_config=None):
    # get launch mode
    mode = os.getenv('FLASK_ENV', "development")

    app = Flask(__name__)

    if not predefined_config:
        app.config.from_object(get_proper_config_name(mode))
    else:
        app.config.from_object(predefined_config)

    # blueprint registration
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_web)
    app.register_blueprint(bp_quiz)

    # database configuration
    database.register_database(app)
    # login manager
    configure_login_manager(app)

    # finally, add context processors
    app = __configure_context_processors(app)

    return app


if __name__ == "__main__":
    quizzing = create_app()
    quizzing.run()

