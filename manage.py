import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from invmanager import create_app, db
from invmanager.models import Group, Permission, User, group_permission, user_group, Token

config_name = os.environ.get('INV_CONFIG', 'production')

app = create_app(config_name=config_name)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(
        app=app,
        db=db,
        Group=Group,
        Permission=Permission,
        User=User,
        Token=Token
    )


manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
