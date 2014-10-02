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
        """ GET /livreurs: exists """

        # Check request
        response = self.get('/livreurs')
        assert response.status_code != 404
        assert response.status_code != 500


class Empty(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_empty(self):
        """ GET /livreurs: empty """

        # Check request
        response = self.get('/livreurs')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 0


class List(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_livreur(id=1)
        build_livreur(id=2)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_livreurs()
        db.session.commit()

    def test_list(self):
        """ GET /livreurs: list """

        # Check request
        response = self.get('/livreurs')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 2

        # Check id
        result_id = [r['id'] for r in result]
        assert 1 in result_id
        assert 2 in result_id