from flask import Blueprint, json, make_response, request
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Country

# Define blueprint
countries = Blueprint('countries', __name__)

# Get list
@countries.route('', methods=['GET', 'OPTIONS'])
def list():
    """ Return all countries.

        Method: *GET*
        URI: */countries*
    """

    # Query
    query = db.session.query(Country)
    countries = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in countries]))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Get one country
@countries.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one country by id.

        Method: *GET*
        URI: */countries/id*
    """

    # Query
    query = db.session.query(Country)
    country = query.get(id)

    # Check country
    if country is None:
        return make_response("Le pays n'existe pas.", 400)

    # Build the response
    response = make_response(jsonify(country.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response