from unittest import TestCase, skip
import uuid

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

        self.user = User()
        self.user.name = "Test Name"
        self.user.email = "test@example.com"
        self.user.password = "test"

        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def test_create_jwt_token(self):
        """
        Tests the creation of a jwt token. Check token is in db as well.

        """

        self.assertEqual(len(self.user.tokens), 0)  # Make sure there are no tokens

        token = self.user.generate_token()
        self.assertIsInstance(token, bytes)

        self.assertEqual(len(self.user.tokens), 1)  # Token should be in db.

        payload = jwt.decode(token, verify=False)

        self.assertIn('token_id', payload)

        token_id = payload['token_id']

        self.assertEqual(self.user.tokens[0].id, uuid.UUID(token_id))

    def test_user_from_jwt(self):
        token = jwt.encode({}, self.app.config['SECRET_KEY'])

        with self.assertRaises(AuthorisationError): # A malformed JWT will throw Authorisation error.
            u = User.from_jwt(token)

        token = jwt.encode({'user_id': 2}, self.app.config['SECRET_KEY'])

        u = User.from_jwt(token)
        self.assertIsNone(u) # If user is not in DB then None is returned.

        token = jwt.encode({'user_id': self.user.id}, self.app.config['SECRET_KEY'])
        u = User.from_jwt(token)
        self.assertIsInstance(u, User)

    @skip("Not Implemented")
    def revoke_jwt(self):
        pass