from webserver import db
from webserver.models import Restaurant
from webserver.tests import build_restaurant
from webserver.tests import delete_restaurants
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
        """ POST /restaurants: exists """

        # Check request
        response = self.post('/restaurants')
        assert response.status_code != 404
        assert response.status_code != 500


class MissingParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_missing_name(self):
        """ POST /restaurants: with missing name """

        # Prepare data
        data = dict()
        data['city'] = "Montreal"
        data['address'] = "1100 Ste-Catherine"
        data['phone'] = "888-888-8888"

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'The name is a mandatory information'

    def test_missing_address(self):
        """ POST /restaurants: with missing address """

        # Prepare data
        data = dict()
        data['name'] = "La Banquise"
        data['city'] = "Montreal"
        data['phone'] = "888-888-8888"

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'The address is a mandatory information'

    def test_missing_city(self):
        """ POST /restaurants: with missing city """

        # Prepare data
        data = dict()
        data['name'] = "La Banquise"
        data['address'] = "1100 Ste-Catherine"
        data['phone'] = "888-888-8888"

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'The city is a mandatory information'

    def test_missing_phone(self):
        """ POST /restaurants: with missing phone """

        # Prepare data
        data = dict()
        data['name'] = "La Banquise"
        data['city'] = "Montreal"
        data['address'] = "1100 Ste-Catherine"

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'The phone is a mandatory information'


class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_invalid_name(self):
        """ POST /restaurants: with invalid name """

        # Prepare data
        data = dict()
        data['name'] = 1
        data['city'] = "Montreal"
        data['address'] = "1100 Ste-Catherine"
        data['phone'] = "888-888-8888"

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'The name must be a string'

    def test_invalid_address(self):
        """ POST /restaurants: with invalid address """

        # Prepare data
        data = dict()
        data['name'] = "La Banquise"
        data['city'] = "Montreal"
        data['address'] = 39940
        data['phone'] = "888-888-8888"

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'The address must be a string'

    def test_invalid_city(self):
        """ POST /restaurants: with invalid city """

        # Prepare data
        data = dict()
        data['name'] = "Restaurant 1"
        data['city'] = 1
        data['address'] = "1100 Ste-Catherine"
        data['phone'] = "888-888-8888"

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'The city must be a string'

    def test_invalid_phone(self):
        """ POST /restaurants: with invalid phone """

        # Prepare data
        data = dict()
        data['name'] = "La Banquise"
        data['city'] = "Montreal"
        data['address'] = "1100 Ste-Catherine"
        data['phone'] = 34.4

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'The phone must be a string'


class Create(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        db.session.commit()

    def test_create(self):
        """ POST /restaurants: with valid data """

        # Prepare data
        data = dict()
        data['name'] = "Restaurant 1"
        data['city'] = "Montreal"
        data['address'] = "1100 Ste-Catherine"
        data['phone'] = "888-888-8888"

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 201

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        restaurant = db.session.query(Restaurant).get(result['id'])
        assert restaurant is not None