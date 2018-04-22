from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db():
    # TODO Add other modules here
    import recorder.api.records.models

    db.init_app(current_app)
    db.create_all()
