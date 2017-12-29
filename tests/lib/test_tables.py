from unittest import TestCase

from invmanager import create_app, db
from invmanager.lib.tables import get_all_table_names
from invmanager.models import Permission


class TestTablesLibrary(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def test_create_permissions(self):
        perms_length = Permission.query.count()
        self.assertEqual(perms_length, 0)  # Make sure no permissions

        self.assertTrue(Permission.create_permissions())

        perms_length = Permission.query.count()
        self.assertGreater(perms_length, 0)

        # Check that calling multiple times does not cause more permissions

        self.assertTrue(Permission.create_permissions())
        perms_length2 = Permission.query.count()

        self.assertEqual(perms_length, perms_length2)

    def test_get_all_tables(self):
        tables = get_all_table_names()

        self.assertGreater(len(tables), 0)

        table_name = tables[0]

        self.assertIn(table_name, tables)

        new_tables = get_all_table_names(ignored_tables=[table_name])

        self.assertNotIn(table_name, new_tables)
