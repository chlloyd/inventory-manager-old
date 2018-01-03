from types import FunctionType
from unittest import TestCase

from flask import g

from invmanager import create_app
from invmanager.auth.decorators import after_request


class TestAuthentication(TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.context = self.app.app_context()
        self.context.push()

        self.client = self.app.test_client()

    def tearDown(self):
        self.context.pop()

    def test_after_request(self):
        called = False

        def view():

            @after_request
            def f(_):
                global called
                called = True
            return ""

        self.app.add_url_rule('/', view_func=view)

        self.client.get('/')

        self.assertGreater(len(g.get('after_request_callbacks')), 0)

        func = g.get('after_request_callbacks')[0]

        self.assertIsInstance(func, FunctionType)
