from flask import Flask
from flask_graphql import GraphQLView
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

    configuration.init_app(app)

    db.init_app(app)

    from invmanager.schema import schema
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=app.debug))

    return app
