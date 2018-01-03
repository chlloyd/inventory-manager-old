import datetime
from unittest import TestCase, mock
import uuid

from flask import Request, Response
import jwt

from invmanager import create_app, db
from invmanager.models import Group, Permission, User
from invmanager.auth.authentication import check_token, revoke_token, get_token, set_token
from invmanager.auth.exceptions import AuthorisationError


class TestAuthentication(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

        Permission.create_permissions()
        Group.create_default_groups()

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
        self.app.config['TOKEN_EXPIRY'] = 60  # Set token to expire in 1 minute

        mocked_return_value = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
        self.assertIsInstance(mocked_return_value, datetime.datetime)

        with mock.patch('invmanager.auth.models.datetime') as datetime_mock:
            # Set time to 5 hours behinc so token has expired

            datetime_mock.utcnow.return_value = mocked_return_value

            token = self.user.generate_token()

            decoded_token = jwt.decode(token, verify=False)
            expiry = decoded_token['exp']
            self.assertLess(expiry, datetime.datetime.utcnow().timestamp())

        with self.assertRaises(jwt.ExpiredSignature):
            check_token(token)


class TestCookieAuthMethods(TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

        Permission.create_permissions()
        Group.create_default_groups()

        self.user = User()
        self.user.name = "Test Name"
        self.user.email = "test@example.com"
        self.user.password = "test"

        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def test_get_cookie(self):
        token = self.user.generate_token()

        request = Request({})

        request.cookies = {'token': token}

        t = get_token(request)

        self.assertEqual(t, token)

    def test_set_cookie(self):
        token = self.user.generate_token()

        response = Response()
        set_token(response,token)

        self.assertIn('Set-Cookie', response.headers)
        self.assertIn(token.decode('utf8'), response.headers.get('Set-Cookie'))


class TestHeaderAuthMethod(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

        Permission.create_permissions()
        Group.create_default_groups()

        self.user = User()
        self.user.name = "Test Name"
        self.user.email = "test@example.com"
        self.user.password = "test"

        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def test_get_cookie(self):
        token = self.user.generate_token()

        request = Request({'HTTP_AUTHORIZATION': token})
        # request.headers.extend({'Authorization': token})

        t = get_token(request)

        self.assertEqual(bytes(t, encoding='utf8'), token)

    def test_set_cookie(self):
        token = self.user.generate_token()

        response = Response()
        set_token(response,token)

        t = response.headers.get('Authorization')

        self.assertIn('Authorization', response.headers)
        self.assertEqual(bytes(t, encoding='utf8'), token)
