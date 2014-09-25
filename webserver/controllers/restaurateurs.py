from flask import Blueprint, json, make_response, request
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Restaurateur, Restaurant

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
        return make_response("Le restaurateur n'existe pas.", 400)

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
        return make_response("Le nom du restaurateur est obligatoire.", 400)
    if not isinstance(datas['firstname'], (str, unicode)):
        return make_response("Le nom du restaurateur doit etre une chaine de caractere.", 400)

    # Check lastname
    if 'lastname' not in datas:
        return make_response("Le prenom du restaurateur est obligatoire.", 400)
    if not isinstance(datas['lastname'], (str, unicode)):
        return make_response("Le prenom du restaurateur doit etre une chaine de caractere.", 400)

    # Check mail
    if 'mail' not in datas:
        return make_response("L'adresse mail du restaurateur est obligatoire.", 400)
    if not isinstance(datas['mail'], (str, unicode)):
        return make_response("L'adresse mail du restaurateur doit etre une chaine de caractere.", 400)

    # Check password
    if 'password' not in datas:
        return make_response("Le mot de passe du restaurateur est obligatoire.", 400)
    if not isinstance(datas['password'], (str, unicode)):
        return make_response("Le mot de passe du restaurateur doit etre une chaine de caractere.", 400)

    # Create restaurateur
    restaurateur = Restaurateur(firstname=datas['firstname'], lastname=datas['lastname'], mail=datas['mail'], password=datas['password'])

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response("Le numero de telephone du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.phone = datas['phone']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response("L'adresse du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response("Le code postal du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("La ville du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.city = datas['city']

    # Check country
    if 'country' in datas:
        if not isinstance(datas['country'], (str, unicode)):
            return make_response("Le pays du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.country = datas['country']

    # Add restaurateur
    db.session.add(restaurateur)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le restaurateur ne peut pas etre cree.", 500)

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
        return make_response("Le restaurateur n'existe pas.", 404)

    # Check firstname
    if 'firstname' in datas:
        if not isinstance(datas['firstname'], (str, unicode)):
            return make_response("Le nom du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.firstname = datas['firstname']

    # Check lastname
    if 'lastname' in datas:
        if not isinstance(datas['lastname'], (str, unicode)):
            return make_response("Le prenom du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.lastname = datas['lastname']

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response("Le numero de telephone du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.phone = datas['phone']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response("L'adresse du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response("Le code postal du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("La ville du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.city = datas['city']

    # Check country
    if 'country' in datas:
        if not isinstance(datas['country'], (str, unicode)):
            return make_response("Le pays du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.country = datas['country']

    # Check mail
    if 'mail' in datas:
        if not isinstance(datas['mail'], (str, unicode)):
            return make_response("L'adresse mail du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.mail = datas['mail']

    # Check password
    if 'password' in datas:
        if not isinstance(datas['password'], (str, unicode)):
            return make_response("Le mot de passe du restaurateur doit etre une chaine de caractere.", 400)
        restaurateur.password = datas['password']

    # Check restaurateur
    if 'restaurant_id' in datas:
        try:
            restaurant_id = int(datas['restaurant_id'])
        except Exception:  # pragma: no cover
            return make_response("restaurant_id doit etre un identifiant.", 400)

        restaurant = db.session.query(Restaurant).get(restaurant_id)
        if restaurant is None:
            return make_response("Le restaurant n\'existe pas.", 404)

        if restaurant.restaurateur is not None:
            if restaurant.restaurateur.id != restaurateur.id:
                return make_response("Le restaurant est deja assignee a un restaurateur.", 400)

        restaurateur.restaurant = restaurant
    else:
        restaurateur.restaurant = None

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le restaurateur ne peut pas etre modifie.", 500)

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
        return make_response("Le restaurateur n'existe pas.", 404)

    # Delete restaurateur
    db.session.delete(restaurateur)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le restaurateur ne peut pas etre supprime.", 500)

    # Build the response
    response = make_response(jsonify(restaurateur.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response