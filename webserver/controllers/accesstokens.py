from flask import Blueprint, json, make_response, request, g
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

    # TODO: TO DELETE IF UNECESSARY
    # from flask.ext.auth import AuthUser
    # admin = AuthUser(username='bob')
    # admin.set_and_encrypt_password('lol')
    # g.user = {'bob': admin}

    # Get request values
    datas = request.values

    # Check firstname
    if 'mail' not in datas:
        return make_response("L'adresse mail est obligatoire.", 400)
    if not isinstance(datas['mail'], (str, unicode)):
        return make_response("L'adresse mail doit etre une chaine de caractere.", 400)

    # Check lastname
    if 'password' not in datas:
        return make_response("Le mot de passe est obligatoire.", 400)
    if not isinstance(datas['password'], (str, unicode)):
        return make_response("Le mot de passe doit etre une chaine de caractere.", 400)

    try:
        user = db.session.query(Personne).filter(Personne.mail==datas['mail']).filter(Personne.password==datas['password']).one()
    except:
        return make_response("Echec d'authentification, l'adresse mail ou le mot de passe ne correspondent a aucun utilisateur.", 404)

    # TODO: TO DELETE IF UNECESSARY
    # g.user = user
    #
    # if datas['username'] in g.user:
    #     if g.user[datas['username']].authenticate(datas['password']):
    #         return make_response("Authentification reussi", 200)

    # Build the response
    response = make_response(jsonify(user.to_dict()))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response
