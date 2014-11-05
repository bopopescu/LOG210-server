# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from flask.ext.babel import gettext
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Dish, Menu

# Define blueprint
dishes = Blueprint('dishes', __name__)

# Get list
@dishes.route('', methods=['GET', 'OPTIONS'])
def list():
    """ Return all dishes.

        Method: *GET*
        URI: */dishes*
    """

    # Query
    query = db.session.query(Dish)
    dishes = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in dishes]))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Get one dish
@dishes.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one dish by id.

        Method: *GET*
        URI: */dishes/id*
    """

    # Query
    query = db.session.query(Dish)
    dish = query.get(id)

    # Check dish
    if dish is None:
        return make_response(gettext(u"Le plat n'existe pas."), 400)

    # Build the response
    response = make_response(jsonify(dish.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Create dish
@dishes.route('', methods=['POST', 'OPTIONS'])
def create():
    """ Create dish

        Method: *POST*
        URI: */dishes*
    """

    # Get request values
    datas = request.values

    # Check name
    if 'name' not in datas:
        return make_response(gettext(u"Le nom du plat est obligatoire."), 400)
    if not isinstance(datas['name'], (str, unicode)):
        return make_response(gettext(u"Le nom du plat doit être une chaine de caractère."), 400)

    # Check name
    if 'menu_id' not in datas:
        return make_response(gettext(u"menu_id est obligatoire."), 400)
    try:
        menu_id = int(datas['menu_id'])
        menu = db.session.query(Menu).get(menu_id)
        if menu is None:
            return make_response(gettext(u"Le menu n'existe pas."), 404)
    except:
        return make_response(gettext(u"menu_id doit être un identifiant."), 400)
        
    # Check description
    if not isinstance(datas['description'], (str, unicode)):
        return make_response(gettext(u"La description du plat doit être une chaine de caractère."), 400)

    # Check price
    if 'price' not in datas:
        return make_response(gettext(u"Le prix du plat est obligatoire."), 400)
    if not isinstance(datas['price'], (float, int)):
        return make_response(gettext(u"Le prix du plat doit être numerique."), 400)
    if not datas['price'] >= 0:
        return make_response(gettext(u"Le prix du plat doit être positif."), 400)

    # Create dish
    dish = Dish(name=datas['name'], description = datas['description'], price = datas['price'], menu_id=menu_id)
    
    # Add dish
    db.session.add(dish)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dû a une erreur inconnue, le plat ne peut pas être crée."), 500)

    # Build the response
    response = make_response(jsonify(dish.to_dict()))
    response.status_code = 201
    response.mimetype = 'application/json'

    return response

# Update dish
@dishes.route('/<int:id>', methods=['PUT', 'OPTIONS'])
def update(id):
    """ Update dish

        Method: *PUT*
        URI: */dishes/id*
    """

    # Get request values
    datas = request.values

    # Check dish
    dish = db.session.query(Dish).get(id)
    if dish is None:
        return make_response(gettext(u"Le plat n'existe pas."), 404)

   # Check name
    if 'name' in datas:
        if not isinstance(datas['name'], (str, unicode)):
            return make_response(gettext(u"Le nom du plat doit être une chaine de caractère."), 400)
        dish.name = datas['name']

    # Check description
    if 'description' in datas:
        if not isinstance(datas['description'], (str, unicode)):
            return make_response(gettext(u"La description du plat doit être une chaine de caractère."), 400)
        dish.description = datas['description']

    # Check price
    if 'price' in datas:
        if not isinstance(datas['price'], (float, int)):
            return make_response(gettext(u"Le prix du plat doit être numerique."), 400)
        if not datas['price'] >= 0:
            return make_response(gettext(u"Le prix du plat doit être positif."), 400)
        dish.price = datas['price']


    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dû a une erreur inconnue, le plat ne peut pas être modifie."), 500)

    # Build the response
    response = make_response(jsonify(dish.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Delete a dish
@dishes.route('/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete(id):
    """ Delete one dish by id.

        Method: *DELETE*
        URI: */dishes/id*
    """

    # Query
    query = db.session.query(Dish)
    dish = query.get(id)

    # Check dish
    if dish is None:
        return make_response(gettext(u"Le plat n'existe pas."), 404)

    # Delete dish
    db.session.delete(dish)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dû a une erreur inconnue, le plat ne peut pas être supprimé."), 500)

    # Build the response
    response = make_response(jsonify(dish.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response