import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Base class for configuration objects. All configurations should inherit
    from Config. Values are added by addingclass variables to the class.

    Should not be instantiated anywhere although this shouldn't have any
    effect.

    We set items here that we want configs to default to in case they are not
    defined in subclasses

    """
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """Method that is called to apply further configurations to the app.

        Called after configuration is passed to Flask and before web server
        is run. Can be used to set up logging.

        Arguments:
            app (Flask): Flask web server object

        Returns:
            None
        """
        pass


class DevelopmentConfig(Config):
    """
    Configuration for use during development.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('INV_DEV_DATABASE', 'sqlite:///' +
                                     os.path.join(basedir,
                                                  'data-dev.sqlite'))

    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(Config):
    """
    Configuration for use during testing. Puts flask into testing mode.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('INV_TEST_DATABASE',
                                     'sqlite:///' +
                                     os.path.join(basedir,
                                                  'data-test.sqlite'))

    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    """
    Configuration for use during testing. Puts flask into production mode.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig
}
