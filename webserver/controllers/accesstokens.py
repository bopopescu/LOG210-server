# -*- coding: utf-8 -*-

from flask import Blueprint, json, make_response, request
from flask.ext.login import login_user, logout_user
from webserver import db
from webserver.lib.base import jsonify
from webserver.models import Personne

# Define blueprint
accesstokens = Blueprint('accesstokens', __name__)

# Create client
@accesstokens.route('', methods=['POST', 'OPTIONS'])
def authentication():
    """ Create accesstoken

        Method: *POST*
        URI: */accesstokens*
    """

    # Get request values
    datas = request.values

    # Check firstname
    if 'mail' not in datas:
        return make_response("L'adresse mail est obligatoire.", 400)
    if not isinstance(datas['mail'], (str, unicode)):
        return make_response("L'adresse mail doit être une chaine de caractère.", 400)

    # Check lastname
    if 'password' not in datas:
        return make_response("Le mot de passe est obligatoire.", 400)
    if not isinstance(datas['password'], (str, unicode)):
        return make_response("Le mot de passe doit être une chaine de caractère.", 400)

    try:
        user = db.session.query(Personne).filter(Personne.mail==datas['mail']).filter(Personne.password==datas['password']).one()
    except:
        return make_response("Echec d'authentification, l'adresse mail ou le mot de passe ne correspondent a aucun utilisateur.", 404)

    if not login_user(user):
        return make_response("Dûe à une erreur inconnu, il est impossible de vous connecter.", 404)

    # Build the response
    response = make_response(jsonify(user.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response


@accesstokens.route('', methods=['DELETE', 'OPTIONS'])
def deauthentication():
    """ Delete accesstoken

        Method: *DELETE*
        URI: */accesstokens*
    """

    logout_user()

    # Build the response
    response = make_response()
    response.status_code = 200
    response.mimetype = 'application/json'

    return response
