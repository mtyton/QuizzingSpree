import os

from flask import Flask

from database import database
from apps.auth.login_manager import configure_login_manager
from apps.auth.views import bp as bp_auth


def get_proper_config_name(mode):
    if mode == "development":
        return 'config.DevelopmentConfig'
    return 'config.ProductionConfig'


def create_app(predefined_config=None):
    # get launch mode
    mode = os.getenv('FLASK_ENV', "development")

    app = Flask(__name__)

    if not predefined_config:
        app.config.from_object(get_proper_config_name(mode))
    else:
        app.config.from_object(predefined_config)
    # login manager
    configure_login_manager(app)
    # blueprint registration
    app.register_blueprint(bp_auth)

    return app


if __name__ == "__main__":
    quizzing = create_app()
    quizzing.run()
    # initialze database only if this is the main file
    database.create_database(quizzing)

