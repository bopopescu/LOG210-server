# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Livreur
from webserver.tests import build_livreur
from webserver.tests import delete_livreurs
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
        """ GET /livreurs/id: exists """

        # Check request
        response = self.get('/livreurs/1')
        assert response.status_code != 404
        assert response.status_code != 500


class UnknownParameters(FunctionalTest):
    """  Check unknown parameters """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_unknown_id(self):
        """ GET /livreurs/id: with unknown id """

        # Check request
        response = self.get('/livreurs/666')
        assert response.status_code == 400
        assert response.data == 'Le livreur n\'existe pas.'


class Get(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_livreur(id=1)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_livreurs()
        db.session.commit()

    def test_get(self):
        """ GET /livreurs/id: with valid data """

        # Check request
        response = self.get('/livreurs/1')
        assert response.status_code == 200

        # Check result
        result = self.parse(response.data)
        assert result is not None

        # Check id
        assert result['id'] == 1