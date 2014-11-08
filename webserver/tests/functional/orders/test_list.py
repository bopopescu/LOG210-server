# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Order
from webserver.tests import build_order, build_state_order, build_client, build_restaurant
from webserver.tests import delete_orders, delete_states_orders, delete_clients, delete_restaurants
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

    def test_invalid_state(self):
        """ PUT /orders?state=1: with invalid state """

        # Check request
        response = self.get('/orders?state=aaa')
        assert response.status_code == 400
        assert response.data == "L'état doit être 0, 1, 2 ou 3."
        
        
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
        
        build_client(id=78)
        build_order(id=5, state=so1, client_id=78)
        build_order(id=6, state=so2, client_id=78)
        
        build_restaurant(id=532)
        build_order(id=15, state=so1, restaurant_id=532)
        
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_orders()
        delete_states_orders()
        delete_clients()
        delete_restaurants()
        
        db.session.commit()

    def test_list(self):
        """ GET /orders: list """

        # Check request
        response = self.get('/orders')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 6

        # Check id
        result_id = [r['id'] for r in result]
        assert 1 in result_id
        assert 2 in result_id
        assert 3 in result_id
        assert 5 in result_id
        assert 6 in result_id
        assert 15 in result_id
        
    def test_list_with_state(self):
        """ GET /orders?state=1: list with state """

        # Check request
        response = self.get('/orders?state=1')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 3

        # Check id
        result_id = [r['id'] for r in result]
        assert 2 in result_id
        assert 3 in result_id
        assert 6 in result_id
        
    def test_list_with_restaurant(self):
        """ GET /orders?restaurant_id=532: list with restaurant_id """

        # Check request
        response = self.get('/orders?restaurant_id=532')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 1

        # Check id
        result_id = [r['id'] for r in result]
        assert 15 in result_id
        
    def test_list_with_client(self):
        """ GET /orders?client_id=78: list with client_id """

        # Check request
        response = self.get('/orders?client_id=78')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 2

        # Check id
        result_id = [r['id'] for r in result]
        assert 5 in result_id
        assert 6 in result_id
        
    def test_list_with_client_and_state(self):
        """ GET /orders?client_id=78&state_id=1: list with client_id """

        # Check request
        response = self.get('/orders?client_id=78&state=1')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 1

        # Check id
        result_id = [r['id'] for r in result]
        assert 6 in result_id