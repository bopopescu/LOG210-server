from flask import Blueprint, json, make_response, request
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Restaurant, Restaurateur

# Define blueprint
restaurants = Blueprint('restaurants', __name__)

# Get list
@restaurants.route('', methods=['GET', 'OPTIONS'])
def list():
    """ Return all restaurants.

        Method: *GET*
        URI: */restaurants*
    """

    # Query
    query = db.session.query(Restaurant)
    restaurants = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in restaurants]))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Get one restaurant
@restaurants.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one restaurant by id.

        Method: *GET*
        URI: */restaurants/id*
    """

    # Query
    query = db.session.query(Restaurant)
    restaurant = query.get(id)

    # Check restaurant
    if restaurant is None:
        return make_response("Le restaurant n'existe pas.", 400)

    # Build the response
    response = make_response(jsonify(restaurant.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Create restaurant
@restaurants.route('', methods=['POST', 'OPTIONS'])
def create():
    """ Create restaurant

        Method: *POST*
        URI: */restaurants*
    """

    # Get request values
    datas = request.values

    # Check name
    if 'name' not in datas:
        return make_response("Le nom du restaurant est obligatoire.", 400)
    if not isinstance(datas['name'], (str, unicode)):
        return make_response("Le nom doit etre une chaine de caractere.", 400)

    # Create restaurant
    restaurant = Restaurant(name=datas['name'])

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response("Le numero de telephone doit etre une chaine de caractere.", 400)
        restaurant.phone = datas['phone']

    # Check cooking type
    if 'cooking_type' in datas:
        if not isinstance(datas['cooking_type'], (str, unicode)):
            return make_response("Le type de cuisine doit etre une chaine de caractere.", 400)
        restaurant.cooking_type = datas['cooking_type']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response("L'adresse doit etre une chaine de caractere.", 400)
        restaurant.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response("Le code postal doit etre une chaine de caractere.", 400)
        restaurant.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("La ville doit etre une chaine de caractere.", 400)
        restaurant.city = datas['city']

    # Check country
    if 'country' in datas:
        if not isinstance(datas['country'], (str, unicode)):
            return make_response("Le pays doit etre une chaine de caractere.", 400)
        restaurant.country = datas['country']

    # Check restaurateur
    if 'restaurateur_id' in datas:
        try:
            restaurateur_id = int(datas['restaurateur_id'])
        except Exception:
            return make_response("restaurateur_id doit etre un identifiant.", 400)

        restaurateur = db.session.query(Restaurateur).get(restaurateur_id)

        if restaurateur is None:
            return make_response("Le restaurateur n\'existe pas.", 404)

        restaurant.restaurateur = restaurateur

    # Add restaurant
    db.session.add(restaurant)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le restaurateur ne peut pas etre cree.", 500)

    # Build the response
    response = make_response(jsonify(restaurant.to_dict()))
    response.status_code = 201
    response.mimetype = 'application/json'

    return response

# Update restaurant
@restaurants.route('/<int:id>', methods=['PUT', 'OPTIONS'])
def update(id):
    """ Update restaurant

        Method: *PUT*
        URI: */restaurants/id*
    """

    # Get request values
    datas = request.values

    # Check restaurant
    restaurant = db.session.query(Restaurant).get(id)
    if restaurant is None:
        return make_response("Le restaurant n'existe pas.", 400)

    # Check name
    if 'name' in datas:
        if not isinstance(datas['name'], (str, unicode)):
            return make_response("Le nom doit etre une chaine de caractere.", 400)

        restaurant.name = datas['name']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("La ville doit etre une chaine de caractere.", 400)

        restaurant.city = datas['city']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response("L'adresse doit etre une chaine de caractere.", 400)

        restaurant.address = datas['address']

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response("Le numero de telephone doit etre une chaine de caractere.", 400)

        restaurant.phone = datas['phone']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response("Le code postal doit etre une chaine de caractere.", 400)
        restaurant.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("La ville doit etre une chaine de caractere.", 400)
        restaurant.city = datas['city']

    # Check country
    if 'country' in datas:
        if not isinstance(datas['country'], (str, unicode)):
            return make_response("Le pays doit etre une chaine de caractere.", 400)
        restaurant.country = datas['country']

    # Check restaurateur
    if 'restaurateur_id' in datas:
        try:
            restaurateur_id = int(datas['restaurateur_id'])
        except Exception:  # pragma: no cover
            return make_response("restaurateur_id doit etre un identifiant.", 400)

        restaurateur = db.session.query(Restaurateur).get(restaurateur_id)

        if restaurateur is None:
            return make_response("Le restaurateur n\'existe pas.", 404)

        restaurant.restaurateur = restaurateur
    else:
        restaurant.restaurateur = None

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le restaurant ne peut pas etre modifie.", 500)

    # Build the response
    response = make_response(jsonify(restaurant.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Delete a restaurant
@restaurants.route('/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete(id):
    """ Delete one restaurant by id.

        Method: *DELETE*
        URI: */restaurants/id*
    """

    # Query
    query = db.session.query(Restaurant)
    restaurant = query.get(id)

    # Check restaurant
    if restaurant is None:
        return make_response("Le restaurant n'existe pas.", 404)

    # Delete restaurant
    db.session.delete(restaurant)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le restaurant ne peut pas etre supprime.", 500)

    # Build the response
    response = make_response(jsonify(restaurant.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response