from unittest import TestCase

from flask import Flask

class TestServer(TestCase):
    def test_server_runs_no_errors(self):
        from invmanager import create_app
        app = create_app('production')
        self.assertIsInstance(app, Flask)
