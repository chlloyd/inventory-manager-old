from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Factory method for creating the web app

    Returns:
        Flask: A Flask web server object

    """
    app = Flask(__name__)
    db.init_app(app)

    return app
