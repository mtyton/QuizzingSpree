from flask_sqlalchemy import SQLAlchemy


"""
This file creates models from all models.py files,
using SqlAlchemy.
"""

db = SQLAlchemy()


def create_database(app):
    db.app = app
    with app.app_context():
        db.init_app(app)
        db.create_all(app=app)
