from flask import Flask


def create_app():
    """Factory method for creating the web app

    Returns:
        Flask: A Flask web server object

    """
    app = Flask(__name__)

    return app
