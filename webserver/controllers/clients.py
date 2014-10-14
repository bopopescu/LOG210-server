# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Client, Country, Personne
import datetime
import gettext

# Define blueprint
clients = Blueprint('clients', __name__)


# Get list
@clients.route('', methods=['GET', 'OPTIONS'])
def list():
    """ Return all clients.

        Method: *GET*
        URI: */clients*
    """

    # Query
    query = db.session.query(Client)
    clients = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in clients]))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# Get one client
@clients.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one client by id.

        Method: *GET*
        URI: */clients/id*
    """

    # Query
    query = db.session.query(Client)
    client = query.get(id)

    # Check client
    if client is None:
        return make_response("Le client n'existe pas.", 400)

    # Build the response
    response = make_response(jsonify(client.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# Create client
@clients.route('', methods=['POST', 'OPTIONS'])
def create():
    """ Create client

        Method: *POST*
        URI: */clients*
    """

    # Get request values
    datas = request.values

    # Check firstname
    if 'firstname' not in datas:
        return make_response("Le nom est obligatoire.", 400)
    if not isinstance(datas['firstname'], (str, unicode)):
        return make_response("Le nom doit être une chaine de caractère.", 400)

    # Check lastname
    if 'lastname' not in datas:
        return make_response("Le prénom est obligatoire.", 400)
    if not isinstance(datas['lastname'], (str, unicode)):
        return make_response("Le prénom doit être une chaine de caractère.", 400)

    # Check mail
    if 'mail' not in datas:
        return make_response("L'adresse mail est obligatoire.", 400)
    if not isinstance(datas['mail'], (str, unicode)):
        return make_response("L'adresse mail doit être une chaine de caractère.", 400)
    if len(db.session.query(Personne).filter(Personne.mail == datas['mail']).all()) > 0:
        return make_response('L\'adresse mail est deja utilisee par un utilisateur.', 400)

    # Check password
    if 'password' not in datas:
        return make_response("Le mot de passe est obligatoire.", 400)
    if not isinstance(datas['password'], (str, unicode)):
        return make_response("Le mot de passe doit être une chaine de caractère.", 400)

    # Check phone
    if 'phone' not in datas:
        return make_response("Le numéro de téléphone est obligatoire.", 400)
    if not isinstance(datas['phone'], (str, unicode)):
        return make_response("Le numéro de téléphone doit être une chaine de caractère.", 400)

    # Check address
    if 'address' not in datas:
        return make_response('L\'adresse est obligatoire.', 400)
    if not isinstance(datas['address'], (str, unicode)):
        return make_response('L\'adresse doit être une chaine de caractère.', 400)

    # Check zipcode
    if 'zipcode' not in datas:
        return make_response('Le code postal est obligatoire.', 400)
    if not isinstance(datas['zipcode'], (str, unicode)):
        return make_response("Le code postal doit être une chaine de caractère.", 400)

    # Check city
    if 'city' not in datas:
        return make_response('La ville est obligatoire.', 400)
    if not isinstance(datas['city'], (str, unicode)):
        return make_response('La ville doit être une chaine de caractère.', 400)

    # Check country
    if 'country_id' not in datas:
        return make_response('Le pays est obligatoire.', 400)
    try:
        country_id = int(datas['country_id'])
    except Exception:
        return make_response("country_id doit être un identifiant.", 400)

    country = db.session.query(Country).get(country_id)
    if country is None:
        return make_response('Le pays n\'existe pas.', 404)

    # Create client
    client = Client(firstname=datas['firstname'], lastname=datas['lastname'], phone=datas['phone'], address=datas['address'], zipcode=datas['zipcode'], city=datas['city'], country=country, mail=datas['mail'], password=datas['password'])

    # Check birthdate
    if 'birthdate' in datas:
        try:
            birthdate = datetime.datetime.strptime(datas['birthdate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return make_response("Le format de la date est invalide.", 400)
        client.birthdate = birthdate

    # Add client
    db.session.add(client)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Dûe à une erreur inconnu, le client ne peut pas être créé.", 500)

    # Build the response
    response = make_response(jsonify(client.to_dict()))
    response.status_code = 201
    response.mimetype = 'application/json'
    return response

# Update client
@clients.route('/<int:id>', methods=['PUT', 'OPTIONS'])
def update(id):
    """ Update client

        Method: *PUT*
        URI: */clients/id*
    """

    # Get request values
    datas = request.values

    # Check client
    client = db.session.query(Client).get(id)
    if client is None:
        return make_response("Le client n'existe pas.", 404)

    # Check firstname
    if 'firstname' in datas:
        if not isinstance(datas['firstname'], (str, unicode)):
            return make_response("Le nom doit être une chaine de caractère.", 400)
        client.firstname = datas['firstname']

    # Check lastname
    if 'lastname' in datas:
        if not isinstance(datas['lastname'], (str, unicode)):
            return make_response("Le prénom doit être une chaine de caractère.", 400)
        client.lastname = datas['lastname']

    # Check password
    if 'password' in datas:
        if not isinstance(datas['password'], (str, unicode)):
            return make_response("Le mot de passe doit être une chaine de caractère.", 400)
        client.password = datas['password']

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response("Le numéro de téléphone doit être une chaine de caractère.", 400)
        client.phone = datas['phone']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response("L'adresse doit être une chaine de caractère.", 400)
        client.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response("Le code postal doit être une chaine de caractère.", 400)
        client.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("La ville doit être une chaine de caractère.", 400)
        client.city = datas['city']

    # Check language
    if 'language' in datas:
        if not isinstance(datas['language'], (str, unicode)):
            return make_response("La langue doit être une chaine de caractère.", 400)
        client.language = datas['language']

    # Check country
    if 'country_id' in datas:
        try:
            country_id = int(datas['country_id'])
        except Exception:  # pragma: no cover
            return make_response("country_id doit être un identifiant.", 400)

        country = db.session.query(Country).get(country_id)
        if country is None:
            return make_response("Le pays n\'existe pas.", 404)
        client.country = country

    # Check birthdate
    if 'birthdate' in datas:
        try:
            birthdate = datetime.datetime.strptime(datas['birthdate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return make_response("Le format de la date est invalide.", 400)
        client.birthdate = birthdate

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Dûe à une erreur inconnu, le client ne peut pas être modifié.", 500)

    # Build the response
    response = make_response(jsonify(client.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# Delete a client
@clients.route('/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete(id):
    """ Delete one client by id.

        Method: *DELETE*
        URI: */clients/id*
    """

    # Query
    query = db.session.query(Client)
    client = query.get(id)

    # Check client
    if client is None:
        return make_response("Le client n'existe pas.", 404)

    # Unlink from country
    client.country = None

    # Delete client
    db.session.delete(client)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Dûe à une erreur inconnu, le client ne peut pas être supprimé.", 500)

    # Build the response
    response = make_response(jsonify(client.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response