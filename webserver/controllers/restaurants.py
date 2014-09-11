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

    # Check circuit
    if restaurant is None:
        return make_response("The restaurant you are trying to target is unknown", 400)

    # Build the response
    response = make_response(jsonify(restaurant.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# # Create restaurant
# @restaurants.route('', methods=['POST', 'OPTIONS'])
# def create():
#     """ Create restaurant
#
#         Method: *POST*
#         URI: */restaurants*
#     """
#
#     # Get request values
#     datas = request.values
#
#     # Check name
#     if 'name' not in datas:
#         return make_response("The name is a mandatory information", 400)
#     if not isinstance(datas['name'], (str, unicode)):
#         return make_response("The name must be a string", 400)
#
#     # Check city
#     if 'city' not in datas:
#         return make_response("The city is a mandatory information", 400)
#     if not isinstance(datas['city'], (str, unicode)):
#         return make_response("The city must be a string", 400)
#
#     # Check country
#     if 'country' not in datas:
#         return make_response("The country is a mandatory information", 400)
#     if not isinstance(datas['country'], (str, unicode)):
#         return make_response("The country must be a string", 400)
#
#     # Create circuit
#     circuit = Circuit(name=datas['name'], city=datas['city'], country=datas['country'])
#
#     # Add circuit
#     db.session.add(circuit)
#
#     # Commit
#     try:
#         db.session.commit()
#     except Exception:  # pragma: no cover
#         db.session.rollback()
#         return make_response("Due to an unexpected error, the circuit cannot be created", 500)
#
#     # Build the response
#     response = make_response(jsonify(circuit.to_dict()))
#     response.status_code = 201
#     response.mimetype = 'application/json'
#
#     return response
#
# # Update restaurant
# @restaurants.route('/<int:id>', methods=['PUT', 'OPTIONS'])
# def update(id):
#     """ Update restaurant
#
#         Method: *PUT*
#         URI: */restaurants/id*
#     """
#
#     # Get request values
#     datas = request.values
#
#     circuit = db.session.query(Circuit).get(id)
#     if circuit is None:
#         return make_response("The circuit you are trying to target is unknown", 400)
#
#     # Check name
#     if 'name' in datas:
#         if not isinstance(datas['name'], (str, unicode)):
#             return make_response("The name must be a string", 400)
#
#         circuit.name = datas['name']
#
#     # Check city
#     if 'city' in datas:
#         if not isinstance(datas['city'], (str, unicode)):
#             return make_response("The city must be a string", 400)
#
#         circuit.city = datas['city']
#
#     # Check country
#     if 'country' in datas:
#         if not isinstance(datas['country'], (str, unicode)):
#             return make_response("The country must be a string", 400)
#
#         circuit.country = datas['country']
#
#     # Commit
#     try:
#         db.session.commit()
#     except Exception:  # pragma: no cover
#         db.session.rollback()
#         return make_response("Due to an unexpected error, the circuit cannot be updated", 500)
#
#     # Build the response
#     response = make_response(jsonify(circuit.to_dict()))
#     response.status_code = 200
#     response.mimetype = 'application/json'
#
#     return response
#
# # Delete a restaurant
# @restaurants.route('/<int:id>', methods=['DELETE', 'OPTIONS'])
# def delete(id):
#     """ Delete one restaurant by id.
#
#         Method: *DELETE*
#         URI: */restaurants/id*
#     """
#
#     # Query
#     query = db.session.query(Circuit)
#     circuit = query.get(id)
#
#     # Check circuit
#     if circuit is None:
#         return make_response("The circuit you are trying to target is unknown", 400)
#
#     # Delete circuit
#     db.session.delete(circuit)
#
#     # Commit
#     try:
#         db.session.commit()
#     except Exception:  # pragma: no cover
#         db.session.rollback()
#         return make_response("Due to an unexpected error, the circuit cannot be updated", 500)
#
#     # Build the response
#     response = make_response(jsonify(circuit.to_dict()))
#     response.status_code = 200
#     response.mimetype = 'application/json'
#
#     return response