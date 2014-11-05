# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from flask.ext.login import AnonymousUserMixin
from flask.ext.babel import gettext
from webserver import db, app
from webserver.lib.base import jsonify
from webserver.models import Order, StateOrder, Client, LineOrder

from twilio.rest import TwilioRestClient 
from webserver.config import TwilioConfig

from sqlalchemy.orm import lazyload

import datetime
import werkzeug

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
        4: Livrée
    """
    
    # Prepare query
    query = db.session.query(Order)
    
    # State
    if 'state' in request.values:
        try:
            state_int = int(request.values['state'])
        except:
            return make_response(gettext(u"L'état doit être 0, 1, 2 ou 3."), 400)
            
        states = {0: u"En attente", 1: u"En préparation", 2: u"Prête", 3: u"En cours de livraison", 4: u"Livrée"}
        state = states[state_int]
        
        query = query.join(StateOrder).filter(StateOrder.name == state)
        
    orders = query.all()

    # Build the response
    response = make_response(jsonify([o.to_dict() for o in orders]))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response
    
    
# Get one order
@orders.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one order by id.

        Method: *GET*
        URI: */orders/id*
    """

    # Query
    query = db.session.query(Order)
    order = query.get(id)

    # Check menu
    if order is None:
        return make_response(gettext(u"La commande n'existe pas."), 400)

    # Build the response
    response = make_response(jsonify(order.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response
    
    
# Create an order
@orders.route('', methods=['POST', 'OPTIONS'])
def create():
    """ Create an order

        Method: *POST*
        URI: */orders*
    """

    # Get request values
    datas = request.values

    # Check date
    if 'date' not in datas:
        return make_response(gettext(u"La date est obligatoire."), 400)
    try:
        date = datetime.datetime.strptime(datas['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        return make_response(gettext(u"Le format de la date est invalide."), 400)

    # Get client id from logged used
    from flask.ext.login import current_user
    if not hasattr(current_user, "id"):
        return make_response(gettext(u"Vous ne pouvez pas passer de commander si vous n'êtes pas connecté."), 400)
        
    # Get state "En attente"
    try:
        state = db.session.query(StateOrder).filter(StateOrder.name=="En attente").one()
    except:
        return make_response(gettext(u"L'état 'En attente' est inexistant."), 400)
        
    # Create menu
    # TODO: generate order number !
    order = Order(number=1, date=date, client_id=current_user.id, state_id=state.id)
    #db.session.flush()
    
    # Create line order
    if 'dishes' not in datas:
        return make_response(gettext(u"Une commande doit comporté au moins un plat."), 400)
        
    for dish in datas['dishes']:
        
        if 'dish_id' not in dish or 'quantity' not in dish:
            return make_response(gettext(u"Une erreur s'est produite."), 400)
            
        try:
            quantity = int(dish['quantity'])
        except:
            return make_response(gettext(u"La quantité doit être un nombre entier."), 400)
            
        try:
            dish_id = int(dish['dish_id'])
        except:
            return make_response(gettext(u"dish_id doit être un identifiant."), 400)
        
        order.lines_order.append(LineOrder(dish_id=dish_id, quantity=quantity))
        
        
    # Add menu
    db.session.add(order)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe a une erreur inconnu, la commande ne peut pas être créée."), 500)

    # Build the response
    response = make_response(jsonify(order.to_dict()))
    response.status_code = 201
    response.mimetype = 'application/json'

    return response
    
    
# Update menu
@orders.route('/<int:id>', methods=['PUT', 'OPTIONS'])
def update(id):
    """ Update order

        Method: *PUT*
        URI: */orders/id*
    """
    
    # Get request values
    datas = request.values

    # Query
    order = db.session.query(Order).get(id)

    # Check menu
    if order is None:
        return make_response(gettext(u"La commande n'existe pas."), 400)
        
    # Check date
    if 'date' in datas:
        try:
            date = datetime.datetime.strptime(datas['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return make_response(gettext(u"Le format de la date est invalide."), 400)
            
        order.date = date
        
    # Check state
    if 'state_id' in datas:
        state = db.session.query(StateOrder).get(datas["state_id"])
        if state is None:
            return make_response(gettext(u"L'état est inexistant."), 400)
            
        order.state_id = state.id
        
        # SMS Notification
        if app.config['TESTING'] is False:  # pragma: no cover
            client = TwilioRestClient(TwilioConfig.ACCOUNT_SID, TwilioConfig.AUTH_TOKEN) 
            client.messages.create(
                to="+15142902316",
                from_="+14387932148",
                body=u"Bonjour votre commande n°%s est passée dans le statut: %s." % (order.number, state.name),
            )
        
    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe a une erreur inconnu, la commande ne peut pas être modifiée."), 500)

    # Build the response
    response = make_response(jsonify(order.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response
    
# Delete a menu
@orders.route('/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete(id):
    """ Delete one order by id.

        Method: *DELETE*
        URI: */orders/id*
    """

    # Query
    query = db.session.query(Order).options(lazyload('*'))
    order = query.get(id)

    # Check menu
    if order is None:
        return make_response(gettext(u"La commande n'existe pas."), 404)
        
    # Delete menu
    db.session.delete(order)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe a une erreur inconnu, la commande ne peut pas être supprimée."), 500)

    # Build the response
    response = make_response(jsonify(order.to_dict(lines_order=False)))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response