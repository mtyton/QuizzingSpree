from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


"""
This file creates models from all models.py files,
using SqlAlchemy.
"""


def init_app(app):
    import ipdb
    ipdb.set_trace()
    with app.app_context():
        db.init_app(app)
        db.create_all(app)
