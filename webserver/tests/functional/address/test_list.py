# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Entrepreneur
from webserver.tests import build_address, build_client
from webserver.tests import delete_addresses, delete_clients
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
        """ GET /addresses: exists """

        # Check request
        response = self.get('/addresses')
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
        """ GET /addresses: empty """

        # Check request
        response = self.get('/addresses')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 0


class List(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_address(id=1)
        build_address(id=2)

        build_client(id=88)
        build_address(id=4, personne_id=88)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_addresses()
        delete_clients()
        
        db.session.commit()

    def test_list(self):
        """ GET /addresses: list """

        # Check request
        response = self.get('/addresses')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 3

        # Check id
        result_id = [r['id'] for r in result]
        assert 1 in result_id
        assert 2 in result_id
        assert 4 in result_id
        
    def test_list_with_personne(self):
        """ GET /addresses?personne_id=id: list with personne_id """

        # Check request
        response = self.get('/addresses?personne_id=88')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 1

        # Check id
        result_id = [r['id'] for r in result]
        assert 4 in result_id