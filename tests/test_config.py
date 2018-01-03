from unittest import TestCase

from flask import Flask

from invmanager import create_app


class TestServer(TestCase):
    def test_config_production(self):
        app = create_app('production')
        context = app.app_context()
        context.push()
        self.assertIsInstance(app, Flask)

        config = app.config

        self.assertFalse(config.get('DEBUG'))
        self.assertFalse(config.get('TESTING'))

        self.assertEqual(config.get('AUTH_METHOD'), 'HEADER')

        context.pop()

    def test_config_development(self):
        app = create_app('development')
        context = app.app_context()
        context.push()
        self.assertIsInstance(app, Flask)

        config = app.config

        self.assertTrue(config.get('DEBUG'))
        self.assertFalse(config.get('TESTING'))

        self.assertEqual(config.get('AUTH_METHOD'), 'COOKIE')

        context.pop()

    def test_config_testing(self):
        app = create_app('testing')
        context = app.app_context()
        context.push()
        self.assertIsInstance(app, Flask)

        config = app.config

        self.assertFalse(config.get('DEBUG'))
        self.assertTrue(config.get('TESTING'))

        self.assertEqual(config.get('AUTH_METHOD'), 'HEADER')

        context.pop()
