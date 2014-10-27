# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from flask.ext.babel import gettext
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Dish

# Define blueprint
menus_dishes = Blueprint('menus_dishes', __name__)

# Get list
@menus_dishes.route('/<int:id>/dishes', methods=['GET', 'OPTIONS'])
def list(id):
    """ Return all dishes for a menu.

        Method: *GET*
        URI: */menus/id/dishes*
    """

    # Query
    query = db.session.query(Dish).filter(Dish.menu_id==id)
    dishes = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in dishes]))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response
