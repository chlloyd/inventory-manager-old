import logging

from flask import current_app
import jwt
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from invmanager import db, Column, Model
from invmanager.auth.exceptions import AuthorisationError
from invmanager.lib.tables import get_all_table_names

logger = logging.getLogger()

group_permission = db.Table('Group_permissions', db.metadata,
                            Column('group_id', db.Integer, db.ForeignKey('Groups.id')),
                            Column('permission_id', db.Integer, db.ForeignKey('Permissions.id'))
                            )

user_group = db.Table('User_groups', db.metadata,
                      Column('user_id', db.Integer, db.ForeignKey('Users.id')),
                      Column('groups_id', db.Integer, db.ForeignKey('Groups.id'))
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

    users = db.relationship('User', secondary=user_group,
                           back_populates="groups")

    def add_permission(self, permission: Permission) -> None:
        """
        Args:
            permission (Permission): Adds Permission to the group

        Returns:
            None

        """
        self.permissions.append(permission)

    def remove_permission(self, permission: Permission) -> None:
        """
        Args:
            permission (Permission): Removes Permission from the group

        Returns:
            None

        """
        self.permissions.remove(permission)


class User(db.Model):
    __tablename__ = 'Users'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)
    email = Column(db.String, unique=True, nullable=False)
    password_hash = Column(db.String, nullable=False)

    groups = db.relationship(Group, secondary=user_group,
                             back_populates="users")

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

        # g = Group.query.filter_by(name='user').first()
        # self.add_group(g)

    @property
    def password(self):
        """

        Raises:
            AttributeError: You cannot access plain text password

        """
        raise AttributeError("Cannot access password")

    @password.setter
    def password(self, password: str):
        """Set the password of the user.
        Generates the hash and stores in database

        Args:
            password: The plain text password

        Returns:
            None

        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verify a password is equal to the hash in the database. Used for logging in.

        Args:
            password: plaintext password

        Returns:
            bool: True if password is equal.

        """
        return check_password_hash(self.password_hash, password)

    def has_group(self, group:str):
        """

        Args:
            group (str): The name of the group. E.g. 'user'

        Returns:
            None

        Raises:


        """
        return group in self.groups

    def add_group(self, g: Group):
        if g is None:
            raise TypeError("Group {g} is None".format(g=g))
        self.groups.append(g)

    def remove_group(self, g: Group):
        self.groups.remove(g)

    @classmethod
    def from_jwt(cls, jwt_token:str):
        decoded = jwt.decode(jwt_token, key=current_app.config.get('SECRET_KEY'), verify=True, algorithms='HS256')

        user_id = decoded.get('user_id', None)

        if user_id is None:
            raise AuthorisationError()

        return User.query.get(user_id)


