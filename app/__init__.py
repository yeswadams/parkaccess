from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config")

    db.init_app(app)

    return app