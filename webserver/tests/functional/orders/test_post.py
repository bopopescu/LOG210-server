# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Order
from webserver.tests import build_order, build_state_order, build_client
from webserver.tests import delete_orders, delete_states_orders, delete_clients
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
        """ POST /orders: exists """

        # Check request
        response = self.post('/orders')
        assert response.status_code != 404
        assert response.status_code != 500


class MissingParameters(FunctionalTest):
    """ Check with no datas """

    pass

    
class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_state_order(id=1, name="En attente")
        build_client(id=12, mail="boby@ets.ca", password="azerty123")
        db.session.commit()
        
    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        delete_states_orders()
        db.session.commit()

    def test_invalid_date(self):
        """ POST /orders: with invalid date """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = 19001012

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "Le format de la date est invalide."

        # Logout user
        self.delete('/accesstokens')
        
        
class BadUsage(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_client(id=12, mail="boby@ets.ca", password="azerty123")
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        db.session.commit()

    def test_no_user_connected(self):
        """ POST /orders: with invalid date """

        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "Vous ne pouvez pas passer de commander si vous n'êtes pas connecté."

    def test_missing_state(self):
        """ POST /orders: with invalid date """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        print response.data
        assert response.data == "L'état 'En attente' est inexistant."

        # Logout user
        self.delete('/accesstokens')
        

class Create(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_state_order(id=1, name="En attente")
        build_client(id=12, mail="boby@ets.ca", password="azerty123")
        
        db.session.commit()
        
    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_orders()
        delete_clients()        
        delete_states_orders()
        
        db.session.commit()

    def test_create(self):
        """ POST /orders: with valid data """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        
        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 201

        # Logout user
        self.delete('/accesstokens')
        
        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        order = db.session.query(Order).get(result['id'])
        assert order is not None