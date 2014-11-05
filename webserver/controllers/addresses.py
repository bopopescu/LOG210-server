# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from flask.ext.babel import gettext
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Address, Country
import datetime

# Define blueprint
addresses = Blueprint('addresses', __name__)


# Get one address
@addresses.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one address by id.

        Method: *GET*
        URI: */address/id*
    """

    # Query
    query = db.session.query(Address)
    address = query.get(id)

    # Check client
    if address is None:
        return make_response(gettext(u"L'adresse n'existe pas."), 400)

    # Build the response
    response = make_response(jsonify(address.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# Create address
@addresses.route('', methods=['POST', 'OPTIONS'])
def create():
    """ Create an address

        Method: *POST*
        URI: */address*
    """

    # Get request values
    datas = request.values

    # Check address
    if 'address' not in datas:
        return make_response(gettext(u"L'adresse est obligatoire."), 400)
    if not isinstance(datas['address'], (str, unicode)):
        return make_response(gettext(u"L'adresse doit être une chaine de caractère."), 400)

    # Check zipcode
    if 'zipcode' not in datas:
        return make_response(gettext(u"Le code postal est obligatoire."), 400)
    if not isinstance(datas['zipcode'], (str, unicode)):
        return make_response(gettext(u"Le code postal doit être une chaine de caractère."), 400)

    # Check city
    if 'city' not in datas:
        return make_response(gettext(u"La ville est obligatoire."), 400)
    if not isinstance(datas['city'], (str, unicode)):
        return make_response(gettext(u"La ville doit être une chaine de caractère."), 400)

    # Check country
    if 'country_id' not in datas:
        return make_response(gettext(u"Le pays est obligatoire."), 400)
    try:
        country_id = int(datas['country_id'])
    except Exception:
        return make_response(gettext(u"country_id doit être un identifiant."), 400)

    country = db.session.query(Country).get(country_id)
    if country is None:
        return make_response(gettext(u"Le pays n'existe pas."), 404)

    # Create address
    address = Address(address=datas['address'], zipcode=datas['zipcode'], city=datas['city'], country=country)

    # Add address
    db.session.add(address)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe à une erreur inconnu, l'adresse ne peut pas être créé."), 500)

    # Build the response
    response = make_response(jsonify(address.to_dict()))
    response.status_code = 201
    response.mimetype = 'application/json'
    return response

# Update address
@addresses.route('/<int:id>', methods=['PUT', 'OPTIONS'])
def update(id):
    """ Update an address by id

        Method: *PUT*
        URI: */address/id*
    """

    # Get request values
    datas = request.values

    # Check address
    address = db.session.query(Address).get(id)
    if address is None:
        return make_response(gettext(u"L'adresse n'existe pas."), 404)

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response(gettext(u"L'adresse doit être une chaine de caractère."), 400)
        address.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response(gettext(u"Le code postal doit être une chaine de caractère."), 400)
        address.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response(gettext(u"La ville doit être une chaine de caractère."), 400)
        address.city = datas['city']

    # Check country
    if 'country_id' in datas:
        try:
            country_id = int(datas['country_id'])
        except Exception:  # pragma: no cover
            return make_response(gettext(u"country_id doit être un identifiant."), 400)

        country = db.session.query(Country).get(country_id)
        if country is None:
            return make_response(gettext(u"Le pays n'existe pas."), 404)
        address.country = country

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe à une erreur inconnu, l'adresse ne peut pas être modifiée."), 500)

    # Build the response
    response = make_response(jsonify(address.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# Delete an address
@addresses.route('/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete(id):
    """ Delete one address by id.

        Method: *DELETE*
        URI: */address/id*
    """

    # Query
    query = db.session.query(Address)
    address = query.get(id)

    # Check client
    if address is None:
        return make_response(gettext(u"L'adresse n'existe pas."), 404)

    # Unlink from country
    address.country = None

    # Delete address
    db.session.delete(address)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe à une erreur inconnu, le client ne peut pas être supprimé."), 500)

    # Build the response
    response = make_response(jsonify(address.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response