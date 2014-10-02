# -*- coding: utf-8 -*-

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

        build_restaurateur(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurateurs()
        db.session.commit()

    def test_exists(self):
        """ DELETE /restaurateurs/id: exists """

        # Check request
        response = self.delete('/restaurateurs/5')
        assert response.status_code != 404
        assert response.status_code != 500


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

    def test_unkown_id(self):
        """ DELETE /restaurateurs/id: with unkown id """

        # Check request
        response = self.delete('/restaurateurs/5')
        assert response.status_code == 404
        assert response.data == 'Le restaurateur n\'existe pas.'


class Delete(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurateur(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurateurs()
        db.session.commit()

    def test_delete(self):
        """ DELETE /restaurateurs/id: with valid data """

        # Check request
        response = self.delete('/restaurateurs/5')
        assert response.status_code == 200

        # Check response
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        restaurateur = db.session.query(Restaurateur).get(result['id'])
        assert restaurateur is None