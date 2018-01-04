from unittest import TestCase

from flask import after_this_request

from invmanager import create_app


class TestDecorators(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()

        self.client = self.app.test_client()

    def tearDown(self):
        self.context.pop()

    def test_after_request_processing(self):
        @self.app.route('/')
        def index():
            @after_this_request
            def foo(response):
                response.headers['X-Foo'] = 'a header'
                return response

            return 'Test'

        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers['X-Foo'], 'a header')
