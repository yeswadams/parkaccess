from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow

from app.models import db
from app.api import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config")

    db.init_app(app)

    return app
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app
