# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from flask.ext.babel import gettext
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Menu, Restaurant

# Define blueprint
restaurants_menus = Blueprint('restaurants_menus', __name__)

# Get list
@restaurants_menus.route('/<int:id>/menus', methods=['GET', 'OPTIONS'])
def list(id):
    """ Return all menus for the specified restaurant.

        Method: *GET*
        URI: */restaurants/id/menus*
    """

    # Check menu id
    if db.session.query(Restaurant).get(id) is None:
        return make_response(gettext(u"Le restaurant n'existe pas."), 404)
        
    # Query
    query = db.session.query(Menu).filter(Menu.restaurant_id == id)
    menus = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in menus]))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response