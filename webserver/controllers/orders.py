# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from flask.ext.babel import gettext
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Order, StateOrder
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
        0: En attente
        1: En préparation
        2: Prête
        3: En cours de livraison
    """
    
    # Prepare query
    query = db.session.query(Order)
    
    # State
    if 'state' in request.values:
        try:
            state_int = int(request.values['state'])
        except:
            return make_response(gettext(u"L'état doit être 0, 1, 2 ou 3."), 400)
            
        states = {0: u"En attente", 1: u"En préparation", 2: u"Prête", 3: u"En cours de livraison"}
        state = states[state_int]
        
        query = query.join(StateOrder).filter(StateOrder.name == state)
        
    orders = query.all()

    # Build the response
    response = make_response(jsonify([o.to_dict() for o in orders]))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response