# -*- coding: utf-8 -*-

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
    
    # Add fixtures
    add_country()
    add_state_order()

    # Add restaurateurs
    from webserver.models import Restaurateur, Country
    ct1 = db.session.query(Country).filter(Country.name=="Canada").one()
    rs1 = Restaurateur(firstname="Valentino", lastname="Rossi", mail="rossi@ducati.it", password="quarantesix", phone="123-456-7890", address="1001 Rue Notre Dame", city="Montreal", zipcode="H3S 1Z1", country=ct1)
    rs2 = Restaurateur(firstname="Fernando", lastname="Alonso", mail="alonso@ferrari.it", password="asturie", phone="123-456-7890", address="1001 Rue Notre Dame", city="Montreal", zipcode="H3S 1Z1", country=ct1)
    db.session.add(rs1)
    db.session.add(rs2)

    # Add entrepreneurs
    from webserver.models import Entrepreneur
    e1 = Entrepreneur(firstname="Jay", lastname="UnNom", mail="un@mail.com", password="passwd", phone="123-456-7890", address="1001 Rue Notre Dame", city="Montreal", zipcode="H3S 1Z1", country=ct1)
    import datetime
    e2 = Entrepreneur(firstname="Entre", lastname="Preneur", mail="entre", password="preneur", phone="123-456-7890", address="1001 Rue Notre Dame", city="Montreal", zipcode="H3S 1Z1", country=ct1, birthdate=datetime.datetime(2010, 10, 10))
    db.session.add(e1)
    db.session.add(e2)

    # Add clients
    from webserver.models import Client
    c1 = Client(firstname="Yvon", lastname="Gagner", mail="gagner@ducati.it", password="passwdc1", phone="123-456-7890", address="1001 Rue Notre Dame", city="Montreal", zipcode="H3S 1Z1", country=ct1)
    c2 = Client(firstname="Leo", lastname="Pard", mail="pard@ferrari.it", password="passwdc2", phone="123-456-7890", address="1001 Rue Notre Dame", city="Montreal", zipcode="H3S 1Z1", country=ct1)
    db.session.add(c1)
    db.session.add(c2)

    # Add restaurants
    from webserver.models import Restaurant
    r1 = Restaurant(name="Subway", phone="514-444-4444", address="1001 Ste-Catherine", city="Montreal", zipcode="H3K 3P2", cooking_type="Fastfood")
    r2 = Restaurant(name="McDonalds", phone="514-444-4444", address="4301 St-Denis", city="Montreal", zipcode="H2S 1R4", cooking_type="Fastfood")
    r3 = Restaurant(name="La Banquise", phone="514-444-4444", address="2167 St-Denis", city="Montreal", zipcode="H4P 2R2", cooking_type="Poutine")
    r4 = Restaurant(name="Le Duc de Lorraine", phone="514-444-4444", address="2983 St-Denis", city="Montreal", zipcode="H1S 1R2", cooking_type="Gastronomie française")
    r5 = Restaurant(name="La Plazza", phone="514-444-4444", address="1893 St-Denis", city="Montreal", zipcode="H4C 2R1", restaurateur=rs2, cooking_type="Plats italiens")
    db.session.add(r1)
    db.session.add(r2)
    db.session.add(r3)
    db.session.add(r4)
    db.session.add(r5)
    
    # Add menus
    from webserver.models import Menu
    m1 = Menu(name="Menu Bigmac", restaurant_id=r5.id)
    db.session.add(m1)
    db.session.flush()
    
    # Add dishes
    from webserver.models import Dish
    d1 = Dish(name="Frites", description="Avec des pomme de terre fraiche", price=4.99, menu_id=m1.id)
    d2 = Dish(name="Bigmac", description="Avec du boeuf tué la veille", price=6.99, menu_id=m1.id)
    d3 = Dish(name="Coca-Cola", description="Du vrai", price=1.99, menu_id=m1.id)
    d4 = Dish(name="Fanta", description="Du vrai", price=1.99, menu_id=m1.id)
    db.session.add(d1)
    db.session.add(d2)
    db.session.add(d3)
    db.session.add(d4)

    db.session.commit()


def add_country():
    """ Add country """

    from webserver.models import Country
    c1 = Country(name="Canada")
    c2 = Country(name="United States")
    db.session.add(c1)
    db.session.add(c2)
    db.session.flush()


def add_state_order():
    """ Add country """

    from webserver.models import StateOrder
    so1 = StateOrder(name="En attente")
    so2 = StateOrder(name="En préparation")
    so3 = StateOrder(name="Prête")
    so4 = StateOrder(name="En cours de livraison")
    db.session.add(so1)
    db.session.add(so2)
    db.session.add(so3)
    db.session.add(so4)
    db.session.flush()


if __name__ == "__main__":
    manager.run()
