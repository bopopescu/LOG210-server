# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Restaurant, Restaurateur
from webserver.tests import build_restaurant, build_restaurateur, build_country
from webserver.tests import delete_restaurants, delete_restaurateurs, delete_countries
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
        assert response.data == 'Le nom du restaurant est obligatoire.'


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

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom doit etre une chaine de caractere.'

    def test_invalid_phone(self):
        """ POST /restaurants: with invalid phone """

        # Prepare data
        data = dict()
        data['name'] = "La Banquise"
        data['phone'] = 948934

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'Le numero de telephone doit etre une chaine de caractere.'

    def test_invalid_cooking_type(self):
        """ POST /restaurants: with invalid cooking type """

        # Prepare data
        data = dict()
        data['name'] = "La Banquise"
        data['cooking_type'] = 948934

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'Le type de cuisine doit etre une chaine de caractere.'

    def test_invalid_address(self):
        """ POST /restaurants: with invalid address """

        # Prepare data
        data = dict()
        data['name'] = "La Banquise"
        data['address'] = 39940

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse doit etre une chaine de caractere.'

    def test_invalid_zipcode(self):
        """ POST /restaurants: with invalid zipcode """

        # Prepare data
        data = dict()
        data['name'] = "La Banquise"
        data['zipcode'] = 39940

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'Le code postal doit etre une chaine de caractere.'

    def test_invalid_city(self):
        """ POST /restaurants: with invalid city """

        # Prepare data
        data = dict()
        data['name'] = "Restaurant 1"
        data['city'] = 1

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'La ville doit etre une chaine de caractere.'

    def test_invalid_country(self):
        """ POST /restaurants: with invalid country """

        # Prepare data
        data = dict()
        data['name'] = "Restaurant 1"
        data['country_id'] = "salut"

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'country_id doit etre un identifiant.'

    def test_invalid_restaurateur(self):
        """ POST /restaurants: with invalid restaurateur_id """

        # Prepare data
        data = dict()
        data['name'] = "La Banquise"
        data['restaurateur_id'] = "salut"

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 400
        assert response.data == 'restaurateur_id doit etre un identifiant.'


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

    def test_unknown_restaurateur(self):
        """ POST /restaurants: with invalid restaurateur """

        # Prepare data
        data = dict()
        data['name'] = "La banquise"
        data['restaurateur_id'] = 999

        # Check request
        response = self.post('/restaurants', data=data)
        print response.status_code
        assert response.status_code== 404
        assert response.data == 'Le restaurateur n\'existe pas.'

    def test_unknown_country(self):
        """ POST /restaurants: with invalid country """

        # Prepare data
        data = dict()
        data['name'] = "La banquise"
        data['country_id'] = 999

        # Check request
        response = self.post('/restaurants', data=data)
        print response.status_code
        assert response.status_code== 404
        assert response.data == 'Le pays n\'existe pas.'


class Create(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_country(id=1, name="Canada")
        build_restaurateur(id=33)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        delete_restaurateurs()
        delete_countries()
        db.session.commit()

    def test_create(self):
        """ POST /restaurants: with valid data """

        # Prepare data
        data = dict()
        data['name'] = "Italia Plaza"
        data['phone'] = "888-888-8888"
        data['cooking_type'] = "Italian food"
        data['address'] = "1100 Ste-Catherine"
        data['zipcode'] = "H1A 1A1"
        data['city'] = "Montreal"
        data['country_id'] = 1

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 201

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        restaurant = db.session.query(Restaurant).get(result['id'])
        assert restaurant is not None

    def test_create_with_restaurateur(self):
        """ POST /restaurants: with valid data """

        # Prepare data
        data = dict()
        data['name'] = "Asia Sky"
        data['phone'] = "888-888-8888"
        data['cooking_type'] = "Asian food"
        data['address'] = "1101 Ste-Catherine"
        data['zipcode'] = "H1A 1A1"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['restaurateur_id'] = 33

        # Check request
        response = self.post('/restaurants', data=data)
        assert response.status_code == 201

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        restaurant = db.session.query(Restaurant).get(result['id'])
        assert restaurant is not None

        # Check restaurant in restaurateur
        restaurateur = db.session.query(Restaurateur).get(33)
        assert restaurateur.restaurant.id == result['id']
