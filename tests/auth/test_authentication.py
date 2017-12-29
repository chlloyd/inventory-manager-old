import datetime
from unittest import TestCase, mock, skip
import uuid

import jwt

from invmanager import create_app, db
from invmanager.models import Permission, User
from invmanager.auth.authentication import check_token, revoke_token
from invmanager.auth.exceptions import AuthorisationError


class TestAuthentication(TestCase):
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

        with self.assertRaises(jwt.InvalidTokenError): # A malformed JWT will throw Authorisation error.
            check_token(token)

        token = jwt.encode({'user_id': 2}, self.app.config['SECRET_KEY'])

        with self.assertRaises(jwt.InvalidTokenError):
            check_token(token)

        token = self.user.generate_token()
        u = check_token(token)
        self.assertIsInstance(u, User)

    def test_revoke_jwt(self):
        """
        Test a non existent token

        Test that revoking a token means that you cannot be authenticated.
        """

        self.assertFalse(revoke_token(uuid.uuid4())) # Random UUID that wont be in DB

        self.assertEqual(len(self.user.tokens), 0)

        token = self.user.generate_token()
        token_id = jwt.decode(token, verify=False)['token_id']

        # Test that the token will authenticate a user
        u = check_token(token)
        self.assertIsInstance(u, User)

        self.assertEqual(len(self.user.tokens), 1)

        revoke_token(token_id)

        with self.assertRaises(AuthorisationError):
            check_token(token)

        self.assertEqual(len(self.user.tokens), 0)  # Token should no longer exist

    def test_expired_token(self):
        self.app.config['TOKEN_EXPIRY'] = 2 * 60 * 60  # Set token to expire in 2 hours


        mocked_return_value = datetime.datetime.utcnow() - datetime.timedelta(hours=3, seconds=1)
        self.assertIsInstance(mocked_return_value, datetime.datetime)
        with mock.patch('datetime.datetime') as datetime_mock:
            # Set time to 3 hours so token has expired

            datetime_mock.utcnow.return_value = mocked_return_value
            print("Mocked current time: ", datetime.datetime.utcnow())
            print("Expiry in seconds: ", self.app.config['TOKEN_EXPIRY'])

            token = self.user.generate_token()

            decoded_token = jwt.decode(token, verify=False)
            expiry = decoded_token['exp']
            print(token)

        with self.assertRaises(jwt.ExpiredSignature):
            check_token(token)
