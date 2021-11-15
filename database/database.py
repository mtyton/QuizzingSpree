from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


"""
This file creates models from all models.py files,
using SqlAlchemy.
"""


def init_app(app):
    db.init_app(app)
    db.create_all(app)
