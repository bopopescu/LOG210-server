from webserver import db
from webserver.models import Restaurateur
from webserver.tests import build_restaurateur
from webserver.tests import delete_restaurateurs
from webserver.tests.functional import FunctionalTest


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_exists(self):
        """ POST /accesstokens: exists """

        # Check request
        response = self.post('/accesstokens')
        assert response.status_code != 404
        assert response.status_code != 500


class MissingParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_missing_mail(self):
        """ POST /accesstokens: with missing mail """

        # Prepare data
        data = dict()
        data['password'] = "azerty"

        # Check request
        response = self.post('/accesstokens', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse mail est obligatoire.'

    def test_missing_password(self):
        """ POST /accesstokens: with missing password """

        # Prepare data
        data = dict()
        data['mail'] = "titi@toto.ca"

        # Check request
        response = self.post('/accesstokens', data=data)
        assert response.status_code == 400
        assert response.data == 'Le mot de passe est obligatoire.'


class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_invalid_mail(self):
        """ POST /accesstokens: with invalid mail """

        # Prepare data
        data = dict()
        data['mail'] = 19090
        data['password'] = "19090"

        # Check request
        response = self.post('/accesstokens', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse mail doit etre une chaine de caractere.'

    def test_invalid_password(self):
        """ POST /accesstokens: with invalid password """

        # Prepare data
        data = dict()
        data['mail'] = "a@a.t"
        data['password'] = 19090

        # Check request
        response = self.post('/accesstokens', data=data)
        assert response.status_code == 400
        assert response.data == 'Le mot de passe doit etre une chaine de caractere.'


class UnknownParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_unknown_user(self):
        """ POST /accesstokens: with invalid user """

        # Prepare data
        data = dict()
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty123"

        # Check request
        response = self.post('/accesstokens', data=data)
        print response.status_code
        assert response.status_code== 404
        assert response.data == 'Echec d\'authentification, l\'adresse mail ou le mot de passe ne correspondent a aucun utilisateur.'


class Valid(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurateur(id=1, mail="bob@boby.fr", password="azerty123")
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurateurs()
        db.session.commit()

    def test_valid(self):
        """ POST /accesstokens: with valid data """

        data = dict()
        data['mail'] = "bob@boby.fr"
        data['password'] = "azerty123"

        # Check request
        response = self.post('/accesstokens', data=data)

        assert response.status_code == 200
