import os

from flask import Flask
from database import database


def get_proper_config_name(mode):
    if mode == "development":
        return 'config.BasicConfig'
    return 'config.ProductionConfig'


def create_app():
    # get launch mode
    mode = os.getenv('FLASK_ENV', "development")

    app = Flask(__name__)
    app.config.from_object(get_proper_config_name(mode))

    # initialize database
    # database.init_app(app)

    # TODO register blueprints
    return app


if __name__ == "__main__":
    create_app().run()
