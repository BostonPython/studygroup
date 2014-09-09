from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager

from studygroup.application import create_app

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
