from flask.ext.script import Manager
from studygroup.application import create_app, db, create_baseline_data


manager = Manager(create_app)


@manager.command
def create_tables():
    db.create_all()
    create_baseline_data()


if __name__ == "__main__":
    manager.run()
