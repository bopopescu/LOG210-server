# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Order
from webserver.tests import build_order, build_state_order, build_client, build_dish, build_address, build_restaurant
from webserver.tests import delete_orders, delete_states_orders, delete_clients, delete_dishes, delete_addresses, delete_restaurants
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
        build_address(id=34)
        build_dish(id=22)
        build_restaurant(id=183)
        
        db.session.commit()
        
    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        delete_dishes()
        delete_clients()        
        delete_states_orders()
        delete_addresses()
        
        db.session.commit()
        
    def test_missing_dishes(self):
        """ POST /orders: with missing dishes """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['address_id'] = 34
        data['restaurant_id'] = 183

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
        data['address_id'] = 34
        data['restaurant_id'] = 183

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
        data['address_id'] = 34
        data['restaurant_id'] = 183

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "Une erreur s'est produite."

        # Logout user
        self.delete('/accesstokens')
        
    def test_missing_address_id(self):
        """ POST /orders: with missing quantity """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'dish_id': 22, 'quantity': 23}]
        data['restaurant_id'] = 183

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "L'adresse de livraison est obligatoire."

        # Logout user
        self.delete('/accesstokens')
        
    def test_missing_restaurant_id(self):
        """ POST /orders: with missing quantity """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'dish_id': 22, 'quantity': 23}]
        data['address_id'] = 34

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "restaurant_id est obligatoire."

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
        build_address(id=55)
        build_restaurant(id=481)
        
        db.session.commit()
        
    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_addresses()
        delete_dishes()
        delete_clients()
        delete_restaurants()
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
        data['address_id'] = 55
        data['restaurant_id'] = 481

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
        data['address_id'] = 55
        data['restaurant_id'] = 481

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
        data['address_id'] = 55
        data['restaurant_id'] = 481

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "La quantité doit être un nombre entier."

        # Logout user
        self.delete('/accesstokens')
        
    def test_invalid_address_id(self):
        """ POST /orders: with invalid address_id """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'dish_id': 23, 'quantity': 1}]
        data['address_id'] = u'aaaa'
        data['restaurant_id'] = 481

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "address_id doit être un identifiant."

        # Logout user
        self.delete('/accesstokens')
        
    def test_invalid_restaurant_id(self):
        """ POST /orders: with invalid restaurant_id """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'dish_id': 23, 'quantity': 1}]
        data['address_id'] = 55
        data['restaurant_id'] = u'aaaa'

        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 400
        assert response.data == "restaurant_id doit être un identifiant."

        # Logout user
        self.delete('/accesstokens')
        
    def test_unknown_address(self):
        """ POST /orders: with unkown address """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'dish_id': 23, 'quantity': 2}]
        data['address_id'] = 544
        data['restaurant_id'] = 481
        
        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 404
        assert response.data == "L'adresse n'existe pas."

        # Logout user
        self.delete('/accesstokens')
        
    def test_unknown_restaurant(self):
        """ POST /orders: with unkown restaurant """

        # Login user
        self.post('/accesstokens', data={'mail': "boby@ets.ca", 'password': "azerty123"})
        
        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'dish_id': 23, 'quantity': 2}]
        data['address_id'] = 55
        data['restaurant_id'] = 544
        
        # Check request
        response = self.post('/orders', data=data)
        assert response.status_code == 404
        assert response.data == "Le restaurant n'existe pas."

        # Logout user
        self.delete('/accesstokens')
        
        
class BadUsage(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_dish(id=59)
        build_client(id=12, mail="boby@ets.ca", password="azerty123")
        build_address(id=544)
        build_restaurant(id=787)
        
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        delete_addresses()
        delete_dishes()
        delete_clients()
        
        db.session.commit()

    def test_no_user_connected(self):
        """ POST /orders: with invalid date """

        # Prepare data
        data = dict()
        data['date'] = "2012-09-03T00:00:00.000Z"
        data['dishes'] = [{'dish_id': 59, 'quantity': 2}]
        data['address_id'] = 544
        data['restaurant_id'] = 787

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
        data['address_id'] = 544
        data['restaurant_id'] = 787
        
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
        build_address(id=444)
        build_restaurant(id=421)
        
        db.session.commit()
        
    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
        delete_orders()
        delete_addresses()
        delete_clients()  
        delete_restaurants()      
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
        data['address_id'] = 444
        data['restaurant_id'] = 421
        
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