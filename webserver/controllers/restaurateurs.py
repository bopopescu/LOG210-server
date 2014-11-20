# -*- coding: utf-8 -*-

from flask import Blueprint, make_response, request
from flask.ext.babel import gettext
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Restaurateur, Restaurant, Country, Personne
import datetime

# Define blueprint
restaurateurs = Blueprint('restaurateurs', __name__)


# Get list
@restaurateurs.route('', methods=['GET', 'OPTIONS'])
def list():
    """ Return all restaurateurs.

        Method: *GET*
        URI: */restaurateurs*
    """

    # Query
    query = db.session.query(Restaurateur)
    restaurateurs = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in restaurateurs]))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response


# Get one restaurateur
@restaurateurs.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one restaurateur by id.

        Method: *GET*
        URI: */restaurateurs/id*
    """

    # Query
    query = db.session.query(Restaurateur)
    restaurateur = query.get(id)

    # Check restaurateur
    if restaurateur is None:
        return make_response(gettext(u"Le restaurateur n'existe pas."), 400)

    # Build the response
    response = make_response(jsonify(restaurateur.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response


# Create restaurateur
@restaurateurs.route('', methods=['POST', 'OPTIONS'])
def create():
    """ Create restaurateur

        Method: *POST*
        URI: */restaurateurs*
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

    # Create restaurateur
    restaurateur = Restaurateur(firstname=datas['firstname'], lastname=datas['lastname'], phone=datas['phone'], address=datas['address'], zipcode=datas['zipcode'], city=datas['city'], country=country, mail=datas['mail'], password=datas['password'])
    db.session.flush()
    restaurateur.create_order_address()

    # Check birthdate
    if 'birthdate' in datas:
        try:
            birthdate = datetime.datetime.strptime(datas['birthdate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return make_response(gettext(u"Le format de la date est invalide."), 400)
        restaurateur.birthdate = birthdate

    # Check restaurant
    if 'restaurant_id' in datas:
        try:
            restaurant_id = int(datas['restaurant_id'])
        except Exception:  # pragma: no cover
            return make_response(gettext(u"restaurant_id doit être un identifiant."), 400)

        restaurant = db.session.query(Restaurant).get(restaurant_id)
        if restaurant is None:
            return make_response(gettext(u"Le restaurant n'existe pas."), 404)
        if restaurant.restaurateur is not None:
            return make_response(gettext(u"Le restaurant est déjà assigné à un restaurateur."), 400)

        restaurateur.restaurant = restaurant

    # Add restaurateur
    db.session.add(restaurateur)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe à une erreur inconnu, le restaurateur ne peut pas être créé."), 500)

    # Build the response
    response = make_response(jsonify(restaurateur.to_dict()))
    response.status_code = 201
    response.mimetype = 'application/json'
    return response


# Update restaurateur
@restaurateurs.route('/<int:id>', methods=['PUT', 'OPTIONS'])
def update(id):
    """ Update restaurateur

        Method: *PUT*
        URI: */restaurateurs/id*
    """

    # Get request values
    datas = request.values

    # Check restaurateur
    restaurateur = db.session.query(Restaurateur).get(id)
    if restaurateur is None:
        return make_response(gettext(u"Le restaurateur n'existe pas."), 404)

    # Check firstname
    if 'firstname' in datas:
        if not isinstance(datas['firstname'], (str, unicode)):
            return make_response(gettext(u"Le nom doit être une chaine de caractère."), 400)
        restaurateur.firstname = datas['firstname']

    # Check lastname
    if 'lastname' in datas:
        if not isinstance(datas['lastname'], (str, unicode)):
            return make_response(gettext(u"Le prénom doit être une chaine de caractère."), 400)
        restaurateur.lastname = datas['lastname']

    # Check mail
    if 'mail' in datas:
        if not isinstance(datas['mail'], (str, unicode)):
            return make_response(gettext(u"L'adresse mail doit être une chaine de caractère."), 400)
        if len(db.session.query(Personne).filter(Personne.mail == datas['mail']).all()) > 1:
            return make_response(gettext(u"L'adresse mail est deja utilisee par un utilisateur."), 400)
        restaurateur.mail = datas['mail']

    # Check password
    if 'password' in datas:
        if not isinstance(datas['password'], (str, unicode)):
            return make_response(gettext(u"Le mot de passe doit être une chaine de caractère."), 400)
        restaurateur.password = datas['password']

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response(gettext(u"Le numéro de téléphone doit être une chaine de caractère."), 400)
        restaurateur.phone = datas['phone']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response(gettext(u"L'adresse doit être une chaine de caractère."), 400)
        restaurateur.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response(gettext(u"Le code postal doit être une chaine de caractère."), 400)
        restaurateur.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response(gettext(u"La ville doit être une chaine de caractère."), 400)
        restaurateur.city = datas['city']

    # Check language
    if 'language' in datas:
        if not isinstance(datas['language'], (str, unicode)):
            return make_response(gettext(u"La langue doit être une chaine de caractère."), 400)
        restaurateur.language = datas['language']

    # Check country
    if 'country_id' in datas:
        try:
            country_id = int(datas['country_id'])
        except Exception:  # pragma: no cover
            return make_response(gettext(u"country_id doit être un identifiant."), 400)

        country = db.session.query(Country).get(country_id)
        if country is None:
            return make_response(gettext(u"Le pays n'existe pas."), 404)
        restaurateur.country = country

    # Check birthdate
    if 'birthdate' in datas:
        try:
            birthdate = datetime.datetime.strptime(datas['birthdate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return make_response(gettext(u"Le format de la date est invalide."), 400)
        restaurateur.birthdate = birthdate

    # Check restaurateur
    if 'restaurant_id' in datas:
        if datas['restaurant_id'] == 'no_restaurant':
            restaurateur.restaurant = None
        else:
            try:
                restaurant_id = int(datas['restaurant_id'])
            except Exception:  # pragma: no cover
                return make_response(gettext(u"restaurant_id doit être un identifiant."), 400)

            restaurant = db.session.query(Restaurant).get(restaurant_id)
            if restaurant is None:
                return make_response(gettext(u"Le restaurant n'existe pas."), 404)

            if restaurant.restaurateur is not None:
                if restaurant.restaurateur.id != restaurateur.id:
                    return make_response(gettext(u"Le restaurant est déjà assigné à un restaurateur."), 400)

            restaurateur.restaurant = restaurant

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe à une erreur inconnu, le restaurateur ne peut pas être modifié."), 500)

    # Build the response
    response = make_response(jsonify(restaurateur.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response


# Delete a restaurateur
@restaurateurs.route('/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete(id):
    """ Delete one restaurateur by id.

        Method: *DELETE*
        URI: */restaurateurs/id*
    """

    # Query
    query = db.session.query(Restaurateur)
    restaurateur = query.get(id)

    # Check restaurateur
    if restaurateur is None:
        return make_response(gettext(u"Le restaurateur n'existe pas."), 404)

    # Unlink from country
    restaurateur.country = None

    # Delete restaurateur
    db.session.delete(restaurateur)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe à une erreur inconnu, le restaurateur ne peut pas être supprimé."), 500)

    # Build the response
    response = make_response(jsonify(restaurateur.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response
