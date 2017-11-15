from unittest import TestCase

from flask import Flask

from invmanager import create_app, db
from invmanager.models import Group, Permission


class TestServer(TestCase):
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
