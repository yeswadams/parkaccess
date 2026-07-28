from flask import Flask

from app.models import db
from app.api import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app
