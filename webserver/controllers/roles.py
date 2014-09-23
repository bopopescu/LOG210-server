from flask import Blueprint, json, make_response, request
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Role

# Define blueprint
roles = Blueprint('roles', __name__)

# Get list
@roles.route('', methods=['GET', 'OPTIONS'])
def list():
    """ Return all roles.

        Method: *GET*
        URI: */roles*
    """

    # Query
    query = db.session.query(Role)
    roles = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in roles]))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Get one role
@roles.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one role by id.

        Method: *GET*
        URI: */roles/id*
    """

    # Query
    query = db.session.query(Role)
    role = query.get(id)

    # Check role
    if role is None:
        return make_response("Le role n'existe pas.", 400)

    # Build the response
    response = make_response(jsonify(role.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response