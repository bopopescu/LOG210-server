# Configuration of Flask application
from webserver import app
from webserver.config import TestingConfig
app.config.from_object(TestingConfig)

# Configure DataBase and create it
from webserver import db
db.initialize(app.config['SQLALCHEMY_DATABASE_URI'])
db.create_all()

# Import models
from webserver.models import Country, Restaurant, Restaurateur, Entrepreneur, Client

# Import others
from datetime import date

# Builders and deleters

# Country
def build_country(id, name="Canada"):
    """ Builder to create a country in database """

    country = Country(id=id, name=name)
    db.session.add(country)

    return country

def delete_countries():
    """ Remove all country from database """

    for country in db.session.query(Country).all():
        db.session.delete(country)

# Restaurateur
def build_restaurateur(id, firstname="Toto", lastname="Bob", phone="444-444-4444", address="1010 Avenue de la banquise", zipcode="H1S1R1", city="Montreal", mail="boby@resto.ca", password="azerty", country=None):
    """ Builder to create a restaurateur in database """

    restaurateur = Restaurateur(id=id, firstname=firstname, lastname=lastname, phone=phone, address=address, zipcode=zipcode, city=city, country=country, mail=mail, password=password)
    db.session.add(restaurateur)

    return restaurateur

def delete_restaurateurs():
    """ Remove all restaurateurs from database """

    for restaurateur in db.session.query(Restaurateur).all():
        db.session.delete(restaurateur)

# Entrepreneur
def build_entrepreneur(id, firstname="Toto", lastname="Bob", phone="444-444-4444", address="1010 Avenue de la banquise", zipcode="H1S1R1", city="Montreal", mail="boby@resto.ca", password="azerty", country=None):
    """ Builder to create a entrepreneur in database """

    entrepreneur = Entrepreneur(id=id, firstname=firstname, lastname=lastname, phone=phone, address=address, zipcode=zipcode, city=city, country=country, mail=mail, password=password)
    db.session.add(entrepreneur)

    return entrepreneur

def delete_entrepreneurs():
    """ Remove all entrepreneurs from database """

    for entrepreneur in db.session.query(Entrepreneur).all():
        db.session.delete(entrepreneur)

# Client
def build_client(id, firstname="Toto", lastname="Bob", phone="444-444-4444", address="1010 Avenue de la banquise", zipcode="H1S1R1", city="Montreal", mail="boby@resto.ca", password="azerty", country=None):
    """ Builder to create a client in database """

    client = Client(id=id, firstname=firstname, lastname=lastname, phone=phone, address=address, zipcode=zipcode, city=city, country=country, mail=mail, password=password)
    db.session.add(client)

    return client

def delete_clients():
    """ Remove all clients from database """

    for client in db.session.query(Client).all():
        db.session.delete(client)

# Restaurant
def build_restaurant(id, name="Resto 1", phone="514-444-4444", cooking_type="Asian cooking", address="1010 Ste-Catherie", zipcode="H1S1R1", city="Montreal", country=None, restaurateur=None):
    """ Builder to create a restaurant in database """

    restaurant = Restaurant(id=id, name=name, phone=phone, cooking_type=cooking_type, address=address, zipcode=zipcode, city=city, country=country, restaurateur=restaurateur)
    db.session.add(restaurant)

    return restaurant

def delete_restaurants():
    """ Remove all restaurant from database """

    for restaurant in db.session.query(Restaurant).all():
        restaurant.restaurateur = None
        db.session.delete(restaurant)