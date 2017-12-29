from unittest import TestCase, skip

from invmanager import create_app, db
from invmanager.models import Group, Permission, User


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

    def test_Group_add_permission(self):
        g = Group()

        db.session.add(g)
        db.session.commit()

        self.assertEqual(len(g.permissions), 0)

        p = Permission.query.filter_by(table_name='Groups', perm_type='create').first()

        self.assertIsNotNone(p)
        self.assertTrue(isinstance(p, Permission))

        g.add_permission(p)

        db.session.commit()

        self.assertEqual(len(g.permissions), 1)

        # Adding the permission again should still be one

        g.add_permission(p)
        db.session.commit()
        self.assertEqual(len(g.permissions), 1)

    def test_Group_remove_permission(self):
        """
        First we add a permission to a group. Then see if removing it actually removes it

        """
        g = Group()

        db.session.add(g)
        db.session.commit()

        self.assertEqual(len(g.permissions), 0)

        p = Permission.query.filter_by(table_name='Groups', perm_type='create').first()

        self.assertIsNotNone(p)
        self.assertTrue(isinstance(p, Permission))

        g.add_permission(p)

        db.session.commit()

        self.assertEqual(len(g.permissions), 1)

        g.remove_permission(p)

        db.session.commit()

        self.assertEqual(len(g.permissions), 0)


class TestUser(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

        Permission.create_permissions()
        Group.create_default_groups()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def test_user_authentication(self):
        password = "password"

        u = User()
        u.name = "Test User"
        u.password = password
        u.email = "test@example.com"

        db.session.add(u)
        db.session.commit()

        self.assertNotEqual(u.password_hash, password)

        self.assertTrue(u.verify_password(password))

    def test_user_get_password(self):
        """Make sure getting a password raises Error
        Returns:

        """
        u = User()
        u.name = "Test User"
        u.password = "password"
        u.email = "test@example.com"

        db.session.add(u)
        db.session.commit()

        with self.assertRaises(AttributeError):
            _ = u.password

    def test_user_add_group(self):
        u = User()
        u.name = "Test User"
        u.password = "password"
        u.email = "test@example.com"

        db.session.add(u)
        db.session.commit()

        self.assertTrue(u.has_group('user'))

        g = Group.query.filter_by(name='admin').first()

        self.assertIsNotNone(g)

        u.add_group(g)
        db.session.commit()
        self.assertTrue(u.has_group('user'))
        self.assertTrue(u.has_group('admin'))

    @skip("Not implemented")
    def test_user_remove_group(self):
        # u = User()
        # u.name = "Test User"
        # u.password = "password"
        # u.email = "test@example.com"
        #
        # db.session.add(u)
        # db.session.commit()
        #
        # self.assertTrue(u.has_group('user'))
        #
        # g = Group.query.filter_by(name='user').first()
        #
        # u.remove_group(g)
        # self.assertFalse(u.has_group('user'))
        pass
