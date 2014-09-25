from flask import Blueprint, json, make_response, request
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Entrepreneur

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
        return make_response("Le entrepreneur n'existe pas.", 400)

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
        return make_response("Le nom du entrepreneur est obligatoire.", 400)
    if not isinstance(datas['firstname'], (str, unicode)):
        return make_response("Le nom du entrepreneur doit etre une chaine de caractere.", 400)

    # Check lastname
    if 'lastname' not in datas:
        return make_response("Le prenom du entrepreneur est obligatoire.", 400)
    if not isinstance(datas['lastname'], (str, unicode)):
        return make_response("Le prenom du entrepreneur doit etre une chaine de caractere.", 400)

    # Check mail
    if 'mail' not in datas:
        return make_response("L'adresse mail du entrepreneur est obligatoire.", 400)
    if not isinstance(datas['mail'], (str, unicode)):
        return make_response("L'adresse mail du entrepreneur doit etre une chaine de caractere.", 400)

    # Check password
    if 'password' not in datas:
        return make_response("Le mot de passe du entrepreneur est obligatoire.", 400)
    if not isinstance(datas['password'], (str, unicode)):
        return make_response("Le mot de passe du entrepreneur doit etre une chaine de caractere.", 400)

    # Create entrepreneur
    entrepreneur = Entrepreneur(firstname=datas['firstname'], lastname=datas['lastname'], mail=datas['mail'], password=datas['password'])

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response("Le numero de telephone du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.phone = datas['phone']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response("L'adresse du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response("Le code postal du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("La ville du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.city = datas['city']

    # Check country
    if 'country' in datas:
        if not isinstance(datas['country'], (str, unicode)):
            return make_response("Le pays du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.country = datas['country']

    # Add entrepreneur
    db.session.add(entrepreneur)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le entrepreneur ne peut pas etre cree.", 500)

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
        return make_response("Le entrepreneur n'existe pas.", 404)

    # Check firstname
    if 'firstname' in datas:
        if not isinstance(datas['firstname'], (str, unicode)):
            return make_response("Le nom du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.firstname = datas['firstname']

    # Check lastname
    if 'lastname' in datas:
        if not isinstance(datas['lastname'], (str, unicode)):
            return make_response("Le prenom du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.lastname = datas['lastname']

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response("Le numero de telephone du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.phone = datas['phone']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response("L'adresse du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response("Le code postal du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("La ville du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.city = datas['city']

    # Check country
    if 'country' in datas:
        if not isinstance(datas['country'], (str, unicode)):
            return make_response("Le pays du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.country = datas['country']

    # Check mail
    if 'mail' in datas:
        if not isinstance(datas['mail'], (str, unicode)):
            return make_response("L'adresse mail du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.mail = datas['mail']

    # Check password
    if 'password' in datas:
        if not isinstance(datas['password'], (str, unicode)):
            return make_response("Le mot de passe du entrepreneur doit etre une chaine de caractere.", 400)
        entrepreneur.password = datas['password']

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le entrepreneur ne peut pas etre modifie.", 500)

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
        return make_response("Le entrepreneur n'existe pas.", 404)

    # Delete entrepreneur
    db.session.delete(entrepreneur)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le entrepreneur ne peut pas etre supprime.", 500)

    # Build the response
    response = make_response(jsonify(entrepreneur.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response