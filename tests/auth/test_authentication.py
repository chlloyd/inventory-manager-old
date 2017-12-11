from unittest import TestCase

import jwt

from invmanager import create_app, db
from invmanager.models import Permission, User
from invmanager.auth.exceptions import AuthorisationError


class TestGroup(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

        Permission.create_permissions()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def test_user_from_jwt(self):
        token = jwt.encode({}, self.app.config['SECRET_KEY'])

        with self.assertRaises(AuthorisationError): # A malformed JWT will throw Authorisation error.
            u = User.from_jwt(token)

        token = jwt.encode({'user_id': 1}, self.app.config['SECRET_KEY'])

        u = User.from_jwt(token)
        self.assertIsNone(u) # If user is not in DB then None is returned.

        u = User()
        u.name = "Test Name"
        u.email = "test@example.com"
        u.password = "test"

        db.session.add(u)
        db.session.commit()

        token = jwt.encode({'user_id': 1}, self.app.config['SECRET_KEY'])
        u = User.from_jwt(token)
        self.assertIsInstance(u, User)
