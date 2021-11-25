import os

from flask import Flask
from database import database

from apps.auth import bp as bp_auth


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
    app.register_blueprint(bp_auth)

    # initialize database
    database.init_app(app)

    return app


if __name__ == "__main__":
    create_app().run()
