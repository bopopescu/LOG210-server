from flask import Blueprint, json, make_response, request
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Dish

# Define blueprint
dishes = Blueprint('dishes', __name__)

# Get list
@dishes.route('', methods=['GET', 'OPTIONS'])
def list():
    """ Return all dishes.

        Method: *GET*
        URI: */dishes*
    """

    # Query
    query = db.session.query(Dish)
    dishes = query.all()

    # Build the response
    response = make_response(jsonify([r.to_dict() for r in dishes]))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Get one dish
@dishes.route('/<int:id>', methods=['GET', 'OPTIONS'])
def index(id):
    """ Return one dish by id.

        Method: *GET*
        URI: */dishes/id*
    """

    # Query
    query = db.session.query(Dish)
    dish = query.get(id)

    # Check dish
    if dish is None:
        return make_response("Le dish n'existe pas.", 400)

    # Build the response
    response = make_response(jsonify(dish.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Create dish
@dishes.route('', methods=['POST', 'OPTIONS'])
def create():
    """ Create dish

        Method: *POST*
        URI: */dishes*
    """

    # Get request values
    datas = request.values

    # Check name
    if 'name' not in datas:
        return make_response("Le nom du dish est obligatoire.", 400)
    if not isinstance(datas['name'], (str, unicode)):
        return make_response("Le nom doit etre une chaine de caractere.", 400)

    # Create dish
    dish = Dish(name=datas['name'])

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response("Le numero de telephone doit etre une chaine de caractere.", 400)
        dish.phone = datas['phone']

    # Check cooking type
    if 'cooking_type' in datas:
        if not isinstance(datas['cooking_type'], (str, unicode)):
            return make_response("Le type de cuisine doit etre une chaine de caractere.", 400)
        dish.cooking_type = datas['cooking_type']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response("L'adresse doit etre une chaine de caractere.", 400)
        dish.address = datas['address']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response("Le code postal doit etre une chaine de caractere.", 400)
        dish.zipcode = datas['zipcode']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("La ville doit etre une chaine de caractere.", 400)
        dish.city = datas['city']

    # Check country
    if 'country_id' in datas:
        try:
            country_id = int(datas['country_id'])
        except Exception:  # pragma: no cover
            return make_response("country_id doit etre un identifiant.", 400)

        country = db.session.query(Country).get(country_id)

        if country is None:
            return make_response("Le pays n\'existe pas.", 404)

        dish.country = country

    # Check restaurateur
    if 'restaurateur_id' in datas:
        try:
            restaurateur_id = int(datas['restaurateur_id'])
        except Exception:
            return make_response("restaurateur_id doit etre un identifiant.", 400)

        restaurateur = db.session.query(Restaurateur).get(restaurateur_id)

        if restaurateur is None:
            return make_response("Le restaurateur n\'existe pas.", 404)

        dish.restaurateur = restaurateur

    # Add dish
    db.session.add(dish)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le restaurateur ne peut pas etre cree.", 500)

    # Build the response
    response = make_response(jsonify(dish.to_dict()))
    response.status_code = 201
    response.mimetype = 'application/json'

    return response

# Update dish
@dishes.route('/<int:id>', methods=['PUT', 'OPTIONS'])
def update(id):
    """ Update dish

        Method: *PUT*
        URI: */dishes/id*
    """

    # Get request values
    datas = request.values

    # Check dish
    dish = db.session.query(Dish).get(id)
    if dish is None:
        return make_response("Le dish n'existe pas.", 400)

    # Check name
    if 'name' in datas:
        if not isinstance(datas['name'], (str, unicode)):
            return make_response("Le nom doit etre une chaine de caractere.", 400)

        dish.name = datas['name']

    # Check city
    if 'city' in datas:
        if not isinstance(datas['city'], (str, unicode)):
            return make_response("La ville doit etre une chaine de caractere.", 400)
        dish.city = datas['city']

    # Check address
    if 'address' in datas:
        if not isinstance(datas['address'], (str, unicode)):
            return make_response("L'adresse doit etre une chaine de caractere.", 400)

        dish.address = datas['address']

    # Check phone
    if 'phone' in datas:
        if not isinstance(datas['phone'], (str, unicode)):
            return make_response("Le numero de telephone doit etre une chaine de caractere.", 400)

        dish.phone = datas['phone']

    # Check zipcode
    if 'zipcode' in datas:
        if not isinstance(datas['zipcode'], (str, unicode)):
            return make_response("Le code postal doit etre une chaine de caractere.", 400)
        dish.zipcode = datas['zipcode']

    # Check country
    if 'country_id' in datas:
        try:
            country_id = int(datas['country_id'])
        except Exception:  # pragma: no cover
            return make_response("country_id doit etre un identifiant.", 400)

        country = db.session.query(Country).get(country_id)

        if country is None:
            return make_response("Le pays n\'existe pas.", 404)

        dish.country = country
    else:
        dish.country = None

    # Check restaurateur
    if 'restaurateur_id' in datas:
        try:
            restaurateur_id = int(datas['restaurateur_id'])
        except Exception:  # pragma: no cover
            return make_response("restaurateur_id doit etre un identifiant.", 400)

        restaurateur = db.session.query(Restaurateur).get(restaurateur_id)

        if restaurateur is None:
            return make_response("Le restaurateur n\'existe pas.", 404)

        if restaurateur.dish is not None:
            if restaurateur.dish.id != dish.id:
                return make_response("Le restaurateur est deja assignee a un dish.", 400)

        dish.restaurateur = restaurateur
    else:
        dish.restaurateur = None

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le dish ne peut pas etre modifie.", 500)

    # Build the response
    response = make_response(jsonify(dish.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response

# Delete a dish
@dishes.route('/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete(id):
    """ Delete one dish by id.

        Method: *DELETE*
        URI: */dishes/id*
    """

    # Query
    query = db.session.query(Dish)
    dish = query.get(id)

    # Check dish
    if dish is None:
        return make_response("Le dish n'existe pas.", 404)

    # Unlink restaurateur from dish
    dish.restaurateur = None

    # Delete dish
    db.session.delete(dish)

    # Commit
    try:
        db.session.commit()
    except Exception:  # pragma: no cover
        db.session.rollback()
        return make_response("Due a une erreur inconnu, le dish ne peut pas etre supprime.", 500)

    # Build the response
    response = make_response(jsonify(dish.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response