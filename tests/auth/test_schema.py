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
        mutation login {
          login(email: "{1}", password: "{2}") {
            user {
              id
              email
            }
          }
        }
        '''
        email = 'test@a.com' # different email
        password = 'testpassword'

        login = self.graphql.execute(
            login_mutation,
            variable_values={
                'email': email,
                'password': password
            }
        )

        print(login)

        self.assertIsNotNone(login.get('errors'))