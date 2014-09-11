# Configuration of Flask application
from webserver import app
from webserver.config import TestingConfig
app.config.from_object(TestingConfig)

# Configure DataBase and create it
from webserver import db
db.initialize(app.config['SQLALCHEMY_DATABASE_URI'])
db.create_all()

# Import models
from webserver.models import Restaurant

# Import others
from datetime import date

# Builders and deleters
def build_restaurant(id, name="Resto 1", phone="514-444-4444", address="1010 Ste-Catherie", city="Montreal"):
    """ Builder to create a restaurant in database """

    restaurant = Restaurant(id=id, name=name, phone=phone, address=address, city=city)
    db.session.add(restaurant)
    return restaurant

def delete_restaurants():
    """ Remove all restaurant from database """

    for restaurant in db.session.query(Restaurant).all():
        db.session.delete(restaurant)