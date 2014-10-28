# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Order
from webserver.tests import build_order, build_state_order
from webserver.tests import delete_orders, delete_states_orders
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
        """ GET /orders: exists """

        # Check request
        response = self.get('/orders')
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
        """ GET /orders: empty """

        # Check request
        response = self.get('/orders')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 0


class List(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        so1 = build_state_order(id=8, name=u"En attente")
        so2 = build_state_order(id=10, name=u"En préparation")
        build_order(id=1, state=so1)
        build_order(id=2, state=so2)
        build_order(id=3, state=so2)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_orders()
        delete_states_orders()
        db.session.commit()

    def test_list(self):
        """ GET /orders: list """

        # Check request
        response = self.get('/orders')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 3

        # Check id
        result_id = [r['id'] for r in result]
        assert 1 in result_id
        assert 2 in result_id
        assert 3 in result_id
        
    def test_list_with_state(self):
        """ GET /orders?state=1: list with state """

        # Check request
        response = self.get('/orders?state=1')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 2

        # Check id
        result_id = [r['id'] for r in result]
        assert 2 in result_id
        assert 3 in result_id