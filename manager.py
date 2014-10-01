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
    add_country()

    # Add restaurateurs
    from webserver.models import Restaurateur
    rs1 = Restaurateur(firstname="Valentino", lastname="Rossi", mail="rossi@ducati.it", password="quarantesix")
    rs2 = Restaurateur(firstname="Fernando", lastname="Alonso", mail="alonso@ferrari.it", password="asturie")
    db.session.add(rs1)
    db.session.add(rs2)

    # Add entrepreneurs
    from webserver.models import Entrepreneur
    e1 = Entrepreneur(firstname="Jay", lastname="UnNom", mail="un@mail.com", password="passwd")
    db.session.add(e1)

    # Add clients
    from webserver.models import Client
    c1 = Client(firstname="Yvon", lastname="Gagner", mail="gagner@ducati.it", password="passwdc1")
    c2 = Client(firstname="Leo", lastname="Pard", mail="pard@ferrari.it", password="passwdc2")
    db.session.add(c1)
    db.session.add(c2)

    # Add restaurants
    from webserver.models import Restaurant
    r1 = Restaurant(name="Subway", phone="514-444-4444", address="Ste-Catherine", city="Montreal")
    r2 = Restaurant(name="McDonalds", phone="514-444-4444", address="St-Denis", city="Montreal")
    r3 = Restaurant(name="La Banquise", phone="514-444-4444", address="St-Denis", city="Montreal")
    r4 = Restaurant(name="Le Duc de Lorraine", phone="514-444-4444", address="St-Denis", city="Montreal")
    r5 = Restaurant(name="La Plazza", phone="514-444-4444", address="St-Denis", city="Montreal", restaurateur=rs2)
    db.session.add(r1)
    db.session.add(r2)
    db.session.add(r3)
    db.session.add(r4)
    db.session.add(r5)

    db.session.commit()

def add_country():
    """ Add country """

    from webserver.models import Country
    c1 = Country(name="Canada")
    c2 = Country(name="United States")
    db.session.add(c1)
    db.session.add(c2)

if __name__ == "__main__":
    manager.run()
