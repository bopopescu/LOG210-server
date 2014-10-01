from flask import Blueprint, json, make_response, request
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Client, Country

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
        return make_response("Le nom du client est obligatoire.", 400)
    if not isinstance(datas['firstname'], (str, unicode)):
        return make_response("Le nom du client doit etre une chaine de caractere.", 400)

    # Check lastname
    if 'lastname' not in datas:
        return make_response("Le prenom du client est obligatoire.", 400)
    if not isinstance(datas['lastname'], (str, unicode)):
        return make_response("Le prenom du client doit etre une chaine de caractere.", 400)

    # Check mail
    if 'mail' not in datas:
        return make_response("L'adresse mail du client est obligatoire.", 400)
    if not isinstance(datas['mail'], (str, unicode)):
        return make_response("L'adresse mail du client doit etre une chaine de caractere.", 400)

    # Check password
    if 'password' not in datas:
        return make_response("Le mot de passe du client est obligatoire.", 400)
    if not isinstance(datas['password'], (str, unicode)):
        return make_response("Le mot de passe du client doit etre une chaine de caractere.", 400)

    # Create client
    client = Client(firstname=datas['firstname'], lastname=datas['lastname'], mail=datas['mail'], password=datas['password'])

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response("Le numero de telephone du client doit etre une chaine de caractere.", 400)
        client.phone = datas['phone']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response("L'adresse du client doit etre une chaine de caractere.", 400)
        client.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response("Le code postal du client doit etre une chaine de caractere.", 400)
        client.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("La ville du client doit etre une chaine de caractere.", 400)
        client.city = datas['city']

    # Check country
    if 'country_id' in datas:
        try:
            country_id = int(datas['country_id'])
        except Exception:  # pragma: no cover
            return make_response("country_id doit etre un identifiant.", 400)

        country = db.session.query(Country).get(country_id)

        if country is None:
            return make_response("Le pays n\'existe pas.", 404)

        client.country = country

    # Add client
    db.session.add(client)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le client ne peut pas etre cree.", 500)

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
            return make_response("Le nom du client doit etre une chaine de caractere.", 400)
        client.firstname = datas['firstname']

    # Check lastname
    if 'lastname' in datas:
        if not isinstance(datas['lastname'], (str, unicode)):
            return make_response("Le prenom du client doit etre une chaine de caractere.", 400)
        client.lastname = datas['lastname']

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response("Le numero de telephone du client doit etre une chaine de caractere.", 400)
        client.phone = datas['phone']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response("L'adresse du client doit etre une chaine de caractere.", 400)
        client.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response("Le code postal du client doit etre une chaine de caractere.", 400)
        client.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("La ville du client doit etre une chaine de caractere.", 400)
        client.city = datas['city']

    # Check country
    if 'country_id' in datas:
        try:
            country_id = int(datas['country_id'])
        except Exception:  # pragma: no cover
            return make_response("country_id doit etre un identifiant.", 400)

        country = db.session.query(Country).get(country_id)

        if country is None:
            return make_response("Le pays n\'existe pas.", 404)

        client.country = country
    else:
        client.country = None

    # Check mail
    if 'mail' in datas:
        if not isinstance(datas['mail'], (str, unicode)):
            return make_response("L'adresse mail du client doit etre une chaine de caractere.", 400)
        client.mail = datas['mail']

    # Check password
    if 'password' in datas:
        if not isinstance(datas['password'], (str, unicode)):
            return make_response("Le mot de passe du client doit etre une chaine de caractere.", 400)
        client.password = datas['password']

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le client ne peut pas etre modifie.", 500)

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

    # Delete client
    db.session.delete(client)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le client ne peut pas etre supprime.", 500)

    # Build the response
    response = make_response(jsonify(client.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response