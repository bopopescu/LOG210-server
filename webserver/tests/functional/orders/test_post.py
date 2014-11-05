# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Order
from webserver.tests import build_order, build_state_order, build_client, build_dish
from webserver.tests import delete_orders, delete_states_orders, delete_clients, delete_dishes
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
        
    def test_missing_dishes(self):
        """ POST /orders: with missing dishes """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "Une commande doit comporté au moins un plat."

        # Logout user
        self.delete('/accesstokens')
        
    def test_missing_quantity(self):
        """ POST /orders: with missing quantity """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'dish_id': 23}]

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "Une erreur s'est produite."

        # Logout user
        self.delete('/accesstokens')
        
    def test_missing_dish_id(self):
        """ POST /orders: with missing quantity """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'quantity': 23}]

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "Une erreur s'est produite."

        # Logout user
        self.delete('/accesstokens')

    
class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_dish(id=56)
        build_state_order(id=1, name="En attente")
        build_client(id=12, mail="boby@ets.ca", password="azerty123")
        db.session.commit()
        
    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
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
        data['dishes'] = [{'dish_id': 56, 'quantity': 2}]

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "Le format de la date est invalide."

        # Logout user
        self.delete('/accesstokens')
        
    def test_invalid_dish_id(self):
        """ POST /orders: with invalid dish_id """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'dish_id': 'ahah', 'quantity': 2}]

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "dish_id doit être un identifiant."

        # Logout user
        self.delete('/accesstokens')
        
    def test_invalid_quantity(self):
        """ POST /orders: with invalid dish_id """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'dish_id': 23, 'quantity': 'ahaha'}]

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "La quantité doit être un nombre entier."

        # Logout user
        self.delete('/accesstokens')
        
        
class BadUsage(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_dish(id=59)
        build_client(id=12, mail="boby@ets.ca", password="azerty123")
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
        delete_clients()
        db.session.commit()

    def test_no_user_connected(self):
        """ POST /orders: with invalid date """

        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'dish_id': 59, 'quantity': 2}]

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "Vous ne pouvez pas passer de commander si vous n'êtes pas connecté."

    def test_invalid_state(self):
        """ POST /orders: with invalid date """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'dish_id': 59, 'quantity': 2}]

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "L'état 'En attente' est inexistant."

        # Logout user
        self.delete('/accesstokens')
        

class Create(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_dish(id=98)
        build_dish(id=105)
        build_state_order(id=1, name="En attente")
        build_client(id=12, mail="boby@ets.ca", password="azerty123")
        
        db.session.commit()
        
    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
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
        data['dishes'] = [{'dish_id': 98, 'quantity': 2}, {'dish_id': 105, 'quantity': 1}]
        
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
        
        assert len(order.lines_order) == 2
        ordered_data = sorted(order.lines_order, key=lambda d: d.id)
        
        assert ordered_data[0].dish_id == 98
        assert ordered_data[0].quantity == 2
        
        assert ordered_data[1].dish_id == 105
        assert ordered_data[1].quantity == 1