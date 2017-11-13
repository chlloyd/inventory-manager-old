import logging

from sqlalchemy.exc import IntegrityError

from invmanager import db, Column, Model
from invmanager.lib.tables import get_all_table_names

logger = logging.getLogger()


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

    table_name = Column(db.String(30), nullable=False)
    perm_type = Column(db.String(30), nullable=False)
    column_name = Column(db.String(30))

    __table_args__ = (
        db.PrimaryKeyConstraint('table_name', 'perm_type'),
    )

    @staticmethod
    def create_permissions() -> bool:
        """Creates permissions based upon the tables in the database

        Note that if there are any permissions already in the database then
        no more will be created.

        Returns:
            bool - True for successful operation. False otherwise

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
