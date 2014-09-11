from flask.ext.script import Manager
from webserver import app, db

manager = Manager(app)

@manager.command
def install():
    db.drop_all()
    db.create_all()
    print("Database successfuly installed")

@manager.command
def install_with_data():
    install()

    from webserver.models import Restaurant
    r1 = Restaurant(name="Subway", phone="514-444-4444", address="Ste-Catherine", city="Montreal")
    r2 = Restaurant(name="McDonalds", phone="514-444-4444", address="St-Denis", city="Montreal")

    db.session.add(r1)
    db.session.add(r2)

    db.session.commit()

if __name__ == "__main__":
    manager.run()
