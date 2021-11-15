from flask import Flask
from database import database


def create_app():
    app = Flask(__name__)
    # setup with the configuration provided
    # TODO - provide proper configuration, we should consider
    #  creating a config factory
    # TODO register blueprints
    return app


if __name__ == "__main__":
    create_app().run()
