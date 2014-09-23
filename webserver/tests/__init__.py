# Configuration of Flask application
from webserver import app
from webserver.config import TestingConfig
app.config.from_object(TestingConfig)

# Configure DataBase and create it
from webserver import db
db.initialize(app.config['SQLALCHEMY_DATABASE_URI'])
db.create_all()

# Import models
from webserver.models import Restaurant, Restaurateur, Role

# Import others
from datetime import date

# Builders and deleters
def build_restaurateur(id, firstname="Toto", lastname="Bob", address="1010 Avenue de la banquise", city="Montreal", mail="boby@resto.ca", password="azerty"):
    """ Builder to create a restaurateur in database """

    restaurateur = Restaurateur(id=id, firstname=firstname, lastname=lastname, address=address, city=city, mail=mail, password=password)
    db.session.add(restaurateur)

    return restaurateur

def delete_restaurateurs():
    """ Remove all restaurateurs from database """

    for restaurateur in db.session.query(Restaurateur).all():
        db.session.delete(restaurateur)

def build_restaurant(id, name="Resto 1", phone="514-444-4444", address="1010 Ste-Catherie", city="Montreal", restaurateur=None):
    """ Builder to create a restaurant in database """

    restaurant = Restaurant(id=id, name=name, phone=phone, address=address, city=city, restaurateur=restaurateur)
    db.session.add(restaurant)

    return restaurant

def delete_restaurants():
    """ Remove all restaurant from database """

    for restaurant in db.session.query(Restaurant).all():
        restaurant.restaurateur = None
        db.session.delete(restaurant)

def build_role(id, name="Resto 1"):
    """ Builder to create a role in database """

    role = Role(id=id, name=name)
    db.session.add(role)

    return role

def delete_roles():
    """ Remove all role from database """

    for role in db.session.query(Role).all():
        db.session.delete(role)