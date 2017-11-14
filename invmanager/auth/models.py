import logging

from sqlalchemy.exc import IntegrityError

from invmanager import db, Column, Model
from invmanager.lib.tables import get_all_table_names

logger = logging.getLogger()

group_permission = db.Table('Group_permissions',
                            Column('group_id', db.Integer, db.ForeignKey('Groups.id')),
                            Column('permission_id', db.Integer, db.ForeignKey('Permissions.id'))
                            )


class Permission(Model):
    """
    A permission.

    The default permission are 'create' 'edit' 'delete' for all the tables in the database except:
        alembic_version
        sqlite_master - These two tables do not need to be edited by a user.

    Example:
      Create User permission will be defined as:
        table_name: 'user'
        type: 'create'

      Edit user active column:
        table_name: 'user'
        type: 'edit'
        column_name: 'active'

    """

    __tablename__ = 'Permissions'

    PERMISSION_TYPES = ['create', 'edit', 'delete']

    id = Column(db.Integer, primary_key=True)
    table_name = Column(db.String(30), nullable=False)
    perm_type = Column(db.String(30), nullable=False)
    column_name = Column(db.String(30))

    @staticmethod
    def create_permissions() -> bool:
        """Creates permissions based upon the tables in the database

        Note that if there are any permissions already in the database then
        no more will be created.

        Returns:
            bool: True for successful operation. False otherwise

            Will return false if it didn't add any because there was
            somethings already in the database.

        """

        is_perms = Permission.query.count() > 0

        if is_perms:
            return False

        table_names = get_all_table_names()
        permissions = [Permission(table_name=table_name, perm_type=group_type)
                       for table_name in table_names
                       for group_type in Permission.PERMISSION_TYPES]

        db.session.add_all(permissions)

        try:
            db.session.commit()
        except IntegrityError as e:
            logging.exception("Tried to create permissions.", exc_info=e)
            return False
        return True


class Group(Model):
    """
    A group is a collection of users who are assigned a certain role.

    Default roles include:
        super_admin - can do anything
        admin - can perform many tasks but none involving operations that could cause permanent damage
        user - all users are given this role by default.
    """
    __tablename__ = 'Groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    permissions = db.relationship(Permission,
                                  secondary=group_permission)

    def add_permission(self, permission: Permission) -> None:
        """
        Args:
            permission (Permission): Adds Permission to the group

        Returns:
            None

        """
        self.permissions.append(permission)
