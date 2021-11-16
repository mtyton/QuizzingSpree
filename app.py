import os

from flask import Flask
from database import database


def get_proper_config_name(mode="development"):

    if mode == "development":
        return 'config.BasicConfig'
    return 'config.ProductionConfig'


def create_app():
    # FIXME - this is mockup,
    #  this should be taken as launch parameter
    mode = os.getenv('FLASK_ENV')

    app = Flask(__name__)
    app.config.from_object(get_proper_config_name(mode))

    # initialize database
    # database.init_app(app)

    # TODO register blueprints
    return app


if __name__ == "__main__":
    create_app().run()
