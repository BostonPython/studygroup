from flask.ext.script import Manager
from studygroup.application import create_app, db


manager = Manager(create_app)

@manager.command
def create_tables():
    db.create_all()

if __name__ == "__main__":
    manager.run()
