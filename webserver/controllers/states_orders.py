# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from flask.ext.babel import gettext
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import StateOrder

# Define blueprint
states_orders = Blueprint('states_orders', __name__)

# Get list
@states_orders.route('', methods=['GET', 'OPTIONS'])
def list():
    """ Return all states_orders.

        Method: *GET*
        URI: */orders/states*
    """

    # Query
    query = db.session.query(StateOrder)
    states_orders = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in states_orders]))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Get one country
@states_orders.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one country by id.

        Method: *GET*
        URI: */orders/states/id*
    """

    # Query
    query = db.session.query(StateOrder)
    so = query.get(id)

    # Check country
    if so is None:
        return make_response(gettext(u"L'état n'existe pas."), 400)

    # Build the response
    response = make_response(jsonify(so.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response