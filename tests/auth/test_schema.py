import unittest

from graphene.test import Client

from invmanager import create_app, db
from invmanager.models import Permission, User
from invmanager.auth.exceptions import AuthorisationError
from invmanager.schema import schema


class TestGroup(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

        Permission.create_permissions()

        self.graphql = Client(schema=schema)

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    @unittest.skip("Not implemented at the moment")
    def test_register_schema(self):
        pass

    @unittest.skip("Not working at the moment")
    def test_login_schema(self):
        # Set up a user
        u = User()
        u.name = "Test User"
        u.email = "test@example.com"
        u.password = "testpassword"

        db.session.add(u)
        db.session.commit()

        login_mutation = '''
        mutation LogIn($email: String!, $password: String!) {
          login(email: $email, password: $password) {
            user {
              name
            }
          }
        }
        '''
        email = 'test@a.com' # wrong email
        password = 'testpassword'

        login = self.graphql.execute(
            login_mutation,
            variable_values={
                'email': email,
                'password': password
            }
        )

        errors = login.get('errors')
        self.assertIsInstance(errors, list)
        #TODO