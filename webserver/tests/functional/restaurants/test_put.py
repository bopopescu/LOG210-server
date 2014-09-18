from webserver import db
from webserver.models import Restaurant
from webserver.tests import build_restaurant, build_restaurateur
from webserver.tests import delete_restaurants, delete_restaurateurs
from webserver.tests.functional import FunctionalTest


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurant(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        db.session.commit()

    def test_exists(self):
        """ PUT /restaurants/id: exists """

        # Check request
        response = self.put('/restaurants/5')
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
        """ PUT /restaurants/id: with unkown id """

        # Check request
        response = self.put('/restaurants/5')
        assert response.status_code == 400
        assert response.data == 'The restaurant you are trying to target is unknown'


class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurant(id=5, name="Resto 1")
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        db.session.commit()

    def test_invalid_name(self):
        """ PUT /restaurants/id: with invalid name """

        # Prepare data
        data = dict()
        data['name'] = 1

        # Check request
        response = self.put('/restaurants/5', data=data)
        assert response.status_code == 400
        assert response.data == 'The name must be a string'

    def test_invalid_address(self):
        """ PUT /restaurants/id: with invalid address """

        # Prepare data
        data = dict()
        data['address'] = 14029

        # Check request
        response = self.put('/restaurants/5', data=data)
        assert response.status_code == 400
        assert response.data == 'The address must be a string'

    def test_invalid_city(self):
        """ PUT /restaurants/id: with invalid city """

        # Prepare data
        data = dict()
        data['city'] = 1

        # Check request
        response = self.put('/restaurants/5', data=data)
        assert response.status_code == 400
        assert response.data == 'The city must be a string'

    def test_invalid_phone(self):
        """ PUT /restaurants/id: with invalid phone """

        # Prepare data
        data = dict()
        data['phone'] = 3422.2

        # Check request
        response = self.put('/restaurants/5', data=data)
        assert response.status_code == 400
        assert response.data == 'The phone must be a string'


class Update(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        r1 = build_restaurateur(id=10)
        build_restaurant(id=5, name="La banquise", restaurateur=r1)

        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        db.session.commit()

    def test_update(self):
        """ PUT /restaurants/id: with valid data """

        # Prepare data
        data = dict()
        data['name'] = "Le duc de Lorraine"
        data['phone'] = "514-555-5555"
        data['address'] = "9000 Boulevard de Carrie"
        data['city'] = "Trois-Rivieres"
        data['restaurateur_id'] = 10

        # Check request
        response = self.put('/restaurants/5', data=data)
        assert response.status_code == 200

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        restaurant = db.session.query(Restaurant).get(result['id'])
        assert restaurant.name == 'Le duc de Lorraine'
        assert restaurant.phone == "514-555-5555"
        assert restaurant.address == '9000 Boulevard de Carrie'
        assert restaurant.city == 'Trois-Rivieres'
        assert restaurant.restaurateur_id == 10
