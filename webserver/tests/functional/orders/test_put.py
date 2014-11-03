# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Order
from webserver.tests import build_order, build_state_order, build_client
from webserver.tests import delete_orders, delete_states_orders, delete_clients
from webserver.tests.functional import FunctionalTest

import datetime


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
        """ PUT /orders/id: exists """

        # Check request
        response = self.put('/orders/1')
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

        build_order(id=2)
        build_client(id=12, mail="boby@ets.ca", password="azerty123")
        db.session.commit()
        
    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        delete_orders()
        db.session.commit()

    def test_invalid_date(self):
        """ PUT /orders/id: with invalid date """

        # Login user
        self.put('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = 19001012

        # Check request
        response = self.put('/orders/2', data=data)
        assert response.status_code == 400
        assert response.data == "Le format de la date est invalide."

        # Logout user
        self.delete('/accesstokens')
        
    def test_invalid_state(self):
        """ PUT /orders/id: with invalid date """

        # Login user
        self.put('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['state_id'] = 9749

        # Check request
        response = self.put('/orders/2', data=data)
        assert response.status_code == 400
        assert response.data == "L'état est inexistant."

        # Logout user
        self.delete('/accesstokens')
        

class Update(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_state_order(id=99, name=u"En préparation")
        build_order(id=3)
        build_client(id=12, mail="boby@ets.ca", password="azerty123")
        
        db.session.commit()
        
    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_orders()
        delete_states_orders()
        delete_clients()        
        
        db.session.commit()

    def test_update(self):
        """ PUT /orders/id: with valid data """

        # Login user
        self.put('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['state_id'] = 99
        
        # Check request
        response = self.put('/orders/3', data=data)
        assert response.status_code == 200

        # Logout user
        self.delete('/accesstokens')
        
        # Check received data
        result = self.parse(response.data)
        assert 'id' in result
        
        # Check in database
        order = db.session.query(Order).get(result['id'])
        assert order.date == datetime.datetime(2012, 9, 3)
        assert order.state_id == 99