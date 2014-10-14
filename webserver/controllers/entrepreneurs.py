# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from flask.ext.babel import gettext
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Entrepreneur, Country, Personne
import datetime

# Define blueprint
entrepreneurs = Blueprint('entrepreneurs', __name__)


# Get list
@entrepreneurs.route('', methods=['GET', 'OPTIONS'])
def list():
    """ Return all entrepreneurs.

        Method: *GET*
        URI: */entrepreneurs*
    """

    # Query
    query = db.session.query(Entrepreneur)
    entrepreneurs = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in entrepreneurs]))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# Get one entrepreneur
@entrepreneurs.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one entrepreneur by id.

        Method: *GET*
        URI: */entrepreneurs/id*
    """

    # Query
    query = db.session.query(Entrepreneur)
    entrepreneur = query.get(id)

    # Check entrepreneur
    if entrepreneur is None:
        return make_response(gettext(u"L'entrepreneur n'existe pas."), 400)

    # Build the response
    response = make_response(jsonify(entrepreneur.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# Create entrepreneur
@entrepreneurs.route('', methods=['POST', 'OPTIONS'])
def create():
    """ Create entrepreneur

        Method: *POST*
        URI: */entrepreneurs*
    """

    # Get request values
    datas = request.values

    # Check firstname
    if 'firstname' not in datas:
        return make_response(gettext(u"Le nom est obligatoire."), 400)
    if not isinstance(datas['firstname'], (str, unicode)):
        return make_response(gettext(u"Le nom doit être une chaine de caractère."), 400)

    # Check lastname
    if 'lastname' not in datas:
        return make_response(gettext(u"Le prénom est obligatoire."), 400)
    if not isinstance(datas['lastname'], (str, unicode)):
        return make_response(gettext(u"Le prénom doit être une chaine de caractère."), 400)

    # Check mail
    if 'mail' not in datas:
        return make_response(gettext(u"L'adresse mail est obligatoire."), 400)
    if not isinstance(datas['mail'], (str, unicode)):
        return make_response(gettext(u"L'adresse mail doit être une chaine de caractère."), 400)
    if len(db.session.query(Personne).filter(Personne.mail == datas['mail']).all()) > 0:
        return make_response(gettext(u"L'adresse mail est deja utilisee par un utilisateur."), 400)

    # Check password
    if 'password' not in datas:
        return make_response(gettext(u"Le mot de passe est obligatoire."), 400)
    if not isinstance(datas['password'], (str, unicode)):
        return make_response(gettext(u"Le mot de passe doit être une chaine de caractère."), 400)

    # Check phone
    if 'phone' not in datas:
        return make_response(gettext(u"Le numéro de téléphone est obligatoire."), 400)
    if not isinstance(datas['phone'], (str, unicode)):
        return make_response(gettext(u"Le numéro de téléphone doit être une chaine de caractère."), 400)

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

    # Create entrepreneur
    entrepreneur = Entrepreneur(firstname=datas['firstname'], lastname=datas['lastname'], phone=datas['phone'], address=datas['address'], zipcode=datas['zipcode'], city=datas['city'], country=country, mail=datas['mail'], password=datas['password'])

    # Check birthdate
    if 'birthdate' in datas:
        try:
            birthdate = datetime.datetime.strptime(datas['birthdate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return make_response(gettext(u"Le format de la date est invalide."), 400)
        entrepreneur.birthdate = birthdate

    # Add entrepreneur
    db.session.add(entrepreneur)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe à une erreur inconnu, l'entrepreneur ne peut pas être créé."), 500)

    # Build the response
    response = make_response(jsonify(entrepreneur.to_dict()))
    response.status_code = 201
    response.mimetype = 'application/json'
    return response

# Update entrepreneur
@entrepreneurs.route('/<int:id>', methods=['PUT', 'OPTIONS'])
def update(id):
    """ Update entrepreneur

        Method: *PUT*
        URI: */entrepreneurs/id*
    """

    # Get request values
    datas = request.values

    # Check entrepreneur
    entrepreneur = db.session.query(Entrepreneur).get(id)
    if entrepreneur is None:
        return make_response(gettext(u"L'entrepreneur n'existe pas."), 404)

    # Check firstname
    if 'firstname' in datas:
        if not isinstance(datas['firstname'], (str, unicode)):
            return make_response(gettext(u"Le nom doit être une chaine de caractère."), 400)
        entrepreneur.firstname = datas['firstname']

    # Check lastname
    if 'lastname' in datas:
        if not isinstance(datas['lastname'], (str, unicode)):
            return make_response(gettext(u"Le prénom doit être une chaine de caractère."), 400)
        entrepreneur.lastname = datas['lastname']

    # Check password
    if 'password' in datas:
        if not isinstance(datas['password'], (str, unicode)):
            return make_response(gettext(u"Le mot de passe doit être une chaine de caractère."), 400)
        entrepreneur.password = datas['password']

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response(gettext(u"Le numéro de téléphone doit être une chaine de caractère."), 400)
        entrepreneur.phone = datas['phone']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response(gettext(u"L'adresse doit être une chaine de caractère."), 400)
        entrepreneur.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response(gettext(u"Le code postal doit être une chaine de caractère."), 400)
        entrepreneur.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response(gettext(u"La ville doit être une chaine de caractère."), 400)
        entrepreneur.city = datas['city']

    # Check language
    if 'language' in datas:
        if not isinstance(datas['language'], (str, unicode)):
            return make_response(gettext(u"La langue doit être une chaine de caractère."), 400)
        entrepreneur.language = datas['language']

    # Check country
    if 'country_id' in datas:
        try:
            country_id = int(datas['country_id'])
        except Exception:  # pragma: no cover
            return make_response(gettext(u"country_id doit être un identifiant."), 400)

        country = db.session.query(Country).get(country_id)
        if country is None:
            return make_response(gettext(u"Le pays n'existe pas."), 404)
        entrepreneur.country = country

    # Check birthdate
    if 'birthdate' in datas:
        try:
            birthdate = datetime.datetime.strptime(datas['birthdate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return make_response(gettext(u"Le format de la date est invalide."), 400)
        entrepreneur.birthdate = birthdate

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe à une erreur inconnu, l'entrepreneur ne peut pas être modifié."), 500)

    # Build the response
    response = make_response(jsonify(entrepreneur.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# Delete a entrepreneur
@entrepreneurs.route('/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete(id):
    """ Delete one entrepreneur by id.

        Method: *DELETE*
        URI: */entrepreneurs/id*
    """

    # Query
    query = db.session.query(Entrepreneur)
    entrepreneur = query.get(id)

    # Check entrepreneur
    if entrepreneur is None:
        return make_response(gettext(u"L'entrepreneur n'existe pas."), 404)

    # Unlink from country
    entrepreneur.country = None

    # Delete entrepreneur
    db.session.delete(entrepreneur)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe à une erreur inconnu, l'entrepreneur ne peut pas être supprimé."), 500)

    # Build the response
    response = make_response(jsonify(entrepreneur.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response