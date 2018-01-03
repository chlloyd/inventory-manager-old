import unittest

from graphene.test import Client

from invmanager import create_app, db
from invmanager.models import Group, Permission, User
from invmanager.auth.exceptions import AuthorisationError
from invmanager.schema import schema


class TestQuery(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

        Permission.create_permissions()
        Group.create_default_groups()

        self.graphql = Client(schema=schema)

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def test_query_me(self):
        self.graphql.execute('''
        {
          me
        }
        ''')


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

        Permission.create_permissions()
        Group.create_default_groups()

        self.graphql = Client(schema=schema)

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    # @unittest.skip("Not implemented at the moment")
    # def test_register_schema(self):
    #     pass

    # def test_login_schema_correct(self):
    #     # Set up a user
    #     u = User()
    #     u.name = "Test User"
    #     u.email = "test@example.com"
    #
    #     password = "testpassword"
    #     u.password = password
    #
    #     db.session.add(u)
    #     db.session.commit()
    #
    #     login_mutation = '''
    #     mutation LogIn($email: String!, $password: String!) {
    #       login(email: $email, password: $password) {
    #         user {
    #           name
    #         }
    #       }
    #     }
    #     '''
    #     # Correct Email & Password
    #     login = self.graphql.execute(
    #         login_mutation,
    #         variable_values={
    #             'email': u.email,
    #             'password': password
    #         }
    #     )
    #     self.assertListEqual(login.get('errors'), [])
    #
    #     # Wrong email
    #     email = 'test@a.com'
    #
    #     login = self.graphql.execute(
    #         login_mutation,
    #         variable_values={
    #             'email': email,
    #             'password': password
    #         }
    #     )
    #
    #     errors = login.get('errors')
    #     self.assertIsInstance(errors, list)
    #     self.assertGreater(errors, 0)
    #
    #     # Correct Email, wrong password
    #     login = self.graphql.execute(
    #         login_mutation,
    #         variable_values={
    #             'email': u.email,
    #             'password': 'wrong_password'
    #         }
    #     )
    #
    #     errors = login.get('errors')
    #     self.assertIsInstance(errors, list)
    #     self.assertGreater(errors, 0)

