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


class Valid(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurateur(id=1, mail="bob", password="azerty123")
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurateurs()
        db.session.commit()

    def test_valid(self):
        """ POST /accesstokens: with valid data """

        data = dict()
        data['mail'] = "bob"
        data['password'] = "azerty123"

        # Check request
        response = self.post('/accesstokens', data=data)

        assert response.status_code == 200

    def test_invalid(self):
        """ POST /accesstokens: with valid data """

        data = dict()
        data['mail'] = "bob"
        data['password'] = "aze123"

        # Check request
        response = self.post('/accesstokens', data=data)

        assert response.status_code == 400

