from flask import Blueprint, json, make_response, request
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Restaurant

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
        return make_response("The restaurant you are trying to target is unknown", 400)

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
        return make_response("The name is a mandatory information", 400)
    if not isinstance(datas['name'], (str, unicode)):
      return make_response("The name must be a string", 400)

    # Check city
    if 'city' not in datas:
        return make_response("The city is a mandatory information", 400)
    if not isinstance(datas['city'], (str, unicode)):
        return make_response("The city must be a string", 400)

    # Check country
    if 'address' not in datas:
        return make_response("The address is a mandatory information", 400)
    if not isinstance(datas['address'], (str, unicode)):
        return make_response("The address must be a string", 400)

    # Check phone
    if 'phone' not in datas:
        return make_response("The phone is a mandatory information", 400)
    if not isinstance(datas['phone'], (str, unicode)):
        return make_response("The phone must be a string", 400)

    # Create restaurant
    restaurant = Restaurant(name=datas['name'], city=datas['city'], address=datas['address'], phone=datas['phone'])

    # Add restaurant
    db.session.add(restaurant)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due to an unexpected error, the restaurant cannot be created", 500)

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

    restaurant = db.session.query(Restaurant).get(id)
    if restaurant is None:
        return make_response("The restaurant you are trying to target is unknown", 400)

    # Check name
    if 'name' in datas:
        if not isinstance(datas['name'], (str, unicode)):
            return make_response("The name must be a string", 400)

        restaurant.name = datas['name']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("The city must be a string", 400)

        restaurant.city = datas['city']

    # Check country
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response("The address must be a string", 400)

        restaurant.address = datas['address']

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response("The phone must be a string", 400)

        restaurant.phone = datas['phone']

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due to an unexpected error, the restaurant cannot be updated", 500)

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
        return make_response("The restaurant you are trying to target is unknown", 400)

    # Delete restaurant
    db.session.delete(restaurant)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due to an unexpected error, the restaurant cannot be updated", 500)

    # Build the response
    response = make_response(jsonify(restaurant.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response