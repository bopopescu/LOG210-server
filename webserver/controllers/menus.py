# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from flask.ext.babel import gettext
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Menu

# Define blueprint
menus = Blueprint('menus', __name__)

# Get list
@menus.route('', methods=['GET', 'OPTIONS'])
def list():
    """ Return all menus.

        Method: *GET*
        URI: */menus*
    """

    # Query
    query = db.session.query(Menu)
    menus = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in menus]))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Get one menu
@menus.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one menu by id.

        Method: *GET*
        URI: */menus/id*
    """

    # Query
    query = db.session.query(Menu)
    menu = query.get(id)

    # Check menu
    if menu is None:
        return make_response(gettext(u"Le menu n'existe pas."), 400)

    # Build the response
    response = make_response(jsonify(menu.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Create menu
@menus.route('', methods=['POST', 'OPTIONS'])
def create():
    """ Create menu

        Method: *POST*
        URI: */menus*
    """

    # Get request values
    datas = request.values

    # Check name
    if 'name' not in datas:
        return make_response(gettext(u"Le nom du menu est obligatoire."), 400)
    if not isinstance(datas['name'], (str, unicode)):
        return make_response(gettext(u"Le nom du menu doit être une chaine de caractère."), 400)

    # Create menu
    menu = Menu(name=datas['name'])
    
    # Add menu
    db.session.add(menu)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe a une erreur inconnu, le menu ne peut pas être cree."), 500)

    # Build the response
    response = make_response(jsonify(menu.to_dict()))
    response.status_code = 201
    response.mimetype = 'application/json'

    return response

# Update menu
@menus.route('/<int:id>', methods=['PUT', 'OPTIONS'])
def update(id):
    """ Update menu

        Method: *PUT*
        URI: */menus/id*
    """

    # Get request values
    datas = request.values

    # Check menu
    menu = db.session.query(Menu).get(id)
    if menu is None:
        return make_response(gettext(u"Le menu n'existe pas."), 404)

   # Check name
    if 'name' in datas:
        if not isinstance(datas['name'], (str, unicode)):
            return make_response(gettext(u"Le nom du menu doit être une chaine de caractère."), 400)
        menu.name = datas['name']

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe a une erreur inconnu, le menu ne peut pas être modifie."), 500)

    # Build the response
    response = make_response(jsonify(menu.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Delete a menu
@menus.route('/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete(id):
    """ Delete one menu by id.

        Method: *DELETE*
        URI: */menus/id*
    """

    # Query
    query = db.session.query(Menu)
    menu = query.get(id)

    # Check menu
    if menu is None:
        return make_response(gettext(u"Le menu n'existe pas."), 404)

    # Delete menu
    db.session.delete(menu)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe a une erreur inconnu, le menu ne peut pas être supprime."), 500)

    # Build the response
    response = make_response(jsonify(menu.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response