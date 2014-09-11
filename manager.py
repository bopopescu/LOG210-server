from flask.ext.script import Manager
from webserver import app, db

manager = Manager(app)

@manager.command
def install():
    db.drop_all()
    db.create_all()
    print("Database successfuly installed")

if __name__ == "__main__":
    manager.run()
