from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
Model = db.Model
Column = db.Column


def create_app(config_name):
    """Factory method for creating the web app

    Returns:
        Flask: A Flask web server object

    """
    app = Flask(__name__)
    configuration = config.get(config_name)
    app.config.from_object(configuration)

    db.init_app(app)

    return app
