# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from flask.ext.babel import gettext
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Order
import datetime

# Define blueprint
orders = Blueprint('orders', __name__)


# Get list
@orders.route('', methods=['GET', 'OPTIONS'])
def list():
    """ Return all orders.

        Method: *GET*
        URI: */orders*
        Parameters: state=?
    """

    # Query
    query = db.session.query(Order)
    orders = query.all()

    # Build the response
    response = make_response(jsonify([o.to_dict() for o in orders]))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response