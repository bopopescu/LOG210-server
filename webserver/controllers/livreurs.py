# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from flask.ext.babel import gettext
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Livreur, Country, Personne
import datetime

# Define blueprint
livreurs = Blueprint('livreurs', __name__)


# Get list
@livreurs.route('', methods=['GET', 'OPTIONS'])
def list():
    """ Return all livreurs.

        Method: *GET*
        URI: */livreurs*
    """

    # Query
    query = db.session.query(Livreur)
    livreurs = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in livreurs]))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# Get one livreur
@livreurs.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one livreur by id.

        Method: *GET*
        URI: */livreurs/id*
    """

    # Query
    query = db.session.query(Livreur)
    livreur = query.get(id)

    # Check livreur
    if livreur is None:
        return make_response(gettext(u"Le livreur n'existe pas."), 400)

    # Build the response
    response = make_response(jsonify(livreur.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# Create livreur
@livreurs.route('', methods=['POST', 'OPTIONS'])
def create():
    """ Create livreur

        Method: *POST*
        URI: */livreurs*
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

    # Create livreur
    livreur = Livreur(firstname=datas['firstname'], lastname=datas['lastname'], phone=datas['phone'], address=datas['address'], zipcode=datas['zipcode'], city=datas['city'], country=country, mail=datas['mail'], password=datas['password'])

    # Check birthdate
    if 'birthdate' in datas:
        try:
            birthdate = datetime.datetime.strptime(datas['birthdate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return make_response(gettext(u"Le format de la date est invalide."), 400)
        livreur.birthdate = birthdate

    # Add livreur
    db.session.add(livreur)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe à une erreur inconnu, le livreur ne peut pas être créé."), 500)

    # Build the response
    response = make_response(jsonify(livreur.to_dict()))
    response.status_code = 201
    response.mimetype = 'application/json'
    return response

# Update livreur
@livreurs.route('/<int:id>', methods=['PUT', 'OPTIONS'])
def update(id):
    """ Update livreur

        Method: *PUT*
        URI: */livreurs/id*
    """

    # Get request values
    datas = request.values

    # Check livreur
    livreur = db.session.query(Livreur).get(id)
    if livreur is None:
        return make_response(gettext(u"Le livreur n'existe pas."), 404)

    # Check firstname
    if 'firstname' in datas:
        if not isinstance(datas['firstname'], (str, unicode)):
            return make_response(gettext(u"Le nom doit être une chaine de caractère."), 400)
        livreur.firstname = datas['firstname']

    # Check lastname
    if 'lastname' in datas:
        if not isinstance(datas['lastname'], (str, unicode)):
            return make_response(gettext(u"Le prénom doit être une chaine de caractère."), 400)
        livreur.lastname = datas['lastname']

    # Check password
    if 'password' in datas:
        if not isinstance(datas['password'], (str, unicode)):
            return make_response(gettext(u"Le mot de passe doit être une chaine de caractère."), 400)
        livreur.password = datas['password']

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response(gettext(u"Le numéro de téléphone doit être une chaine de caractère."), 400)
        livreur.phone = datas['phone']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response(gettext(u"L'adresse doit être une chaine de caractère."), 400)
        livreur.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response(gettext(u"Le code postal doit être une chaine de caractère."), 400)
        livreur.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response(gettext(u"La ville doit être une chaine de caractère."), 400)
        livreur.city = datas['city']

    # Check language
    if 'language' in datas:
        if not isinstance(datas['language'], (str, unicode)):
            return make_response(gettext(u"La langue doit être une chaine de caractère."), 400)
        livreur.language = datas['language']

    # Check country
    if 'country_id' in datas:
        try:
            country_id = int(datas['country_id'])
        except Exception:  # pragma: no cover
            return make_response(gettext(u"country_id doit être un identifiant."), 400)

        country = db.session.query(Country).get(country_id)
        if country is None:
            return make_response(gettext(u"Le pays n'existe pas."), 404)
        livreur.country = country

    # Check birthdate
    if 'birthdate' in datas:
        try:
            birthdate = datetime.datetime.strptime(datas['birthdate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return make_response(gettext(u"Le format de la date est invalide."), 400)
        livreur.birthdate = birthdate

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe à une erreur inconnu, le livreur ne peut pas être modifié."), 500)

    # Build the response
    response = make_response(jsonify(livreur.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# Delete a livreur
@livreurs.route('/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete(id):
    """ Delete one livreur by id.

        Method: *DELETE*
        URI: */livreurs/id*
    """

    # Query
    query = db.session.query(Livreur)
    livreur = query.get(id)

    # Check livreur
    if livreur is None:
        return make_response(gettext(u"Le livreur n'existe pas."), 404)

    # Unlink from country
    livreur.country = None

    # Delete livreur
    db.session.delete(livreur)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response(gettext(u"Dûe à une erreur inconnu, le livreur ne peut pas être supprimé."), 500)

    # Build the response
    response = make_response(jsonify(livreur.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response