from threading import Thread
import time
from unittest import TestCase

from flask import Flask

class TestServer(TestCase):
    def test_server_runs_no_errors(self):
        from invmanager import create_app
        app = create_app()
        self.assertIsInstance(app, Flask)
