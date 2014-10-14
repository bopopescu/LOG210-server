# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Restaurateur
from webserver.tests import build_restaurateur, build_restaurant, build_country
from webserver.tests import delete_restaurateurs, delete_restaurateurs, delete_countries
from webserver.tests.functional import FunctionalTest


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurateur(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurateurs()
        db.session.commit()

    def test_exists(self):
        """ PUT /restaurateurs/id: exists """

        # Check request
        response = self.put('/restaurateurs/5')
        assert response.status_code != 404
        assert response.status_code != 500


class UnknownParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurateur(id=15)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurateurs()
        db.session.commit()

    def test_unknown_id(self):
        """ PUT /restaurateurs/id: with unkown id """

        # Check request
        response = self.put('/restaurateurs/5')
        assert response.status_code == 404
        assert response.data == 'Le restaurateur n\'existe pas.'

    def test_unknown_country(self):
        """ PUT /restaurateurs/id: with unkown country_id """

        # Prepare data
        data = dict()
        data['country_id'] = 1111

        # Check request
        response = self.put('/restaurateurs/15', data=data)
        assert response.status_code == 404
        assert response.data == 'Le pays n\'existe pas.'


    def test_unknown_restaurant(self):
        """ PUT /restaurateurs/id: with unkown restaurant_id """

        # Prepare data
        data = dict()
        data['restaurant_id'] = 1111

        # Check request
        response = self.put('/restaurateurs/15', data=data)
        assert response.status_code == 404
        assert response.data == 'Le restaurant n\'existe pas.'


class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurateur(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurateurs()
        db.session.commit()

    def test_invalid_firstname(self):
        """ PUT /restaurateurs/id: with invalid firstname """

        # Prepare data
        data = dict()
        data['firstname'] = 1111

        # Check request
        response = self.put('/restaurateurs/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom doit être une chaine de caractère.'

    def test_invalid_lastname(self):
        """ PUT /restaurateurs/id: with invalid lastname """

        # Prepare data
        data = dict()
        data['lastname'] = 1111

        # Check request
        response = self.put('/restaurateurs/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le prénom doit être une chaine de caractère.'

    def test_invalid_birthdate(self):
        """ PUT /restaurateurs/id: with invalid birthdate """

        # Prepare data
        data = dict()
        data['birthdate'] = 89382

        # Check request
        response = self.put('/restaurateurs/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le format de la date est invalide.'

    def test_invalid_phone(self):
        """ PUT /restaurateurs/id: with invalid phone """

        # Prepare data
        data = dict()
        data['phone'] = 1111

        # Check request
        response = self.put('/restaurateurs/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le numéro de téléphone doit être une chaine de caractère.'

    def test_invalid_address(self):
        """ PUT /restaurateurs/id: with invalid address """

        # Prepare data
        data = dict()
        data['address'] = 1111

        # Check request
        response = self.put('/restaurateurs/5', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse doit être une chaine de caractère.'

    def test_invalid_zipcode(self):
        """ PUT /restaurateurs/id: with invalid zipcode """

        # Prepare data
        data = dict()
        data['zipcode'] = 1111

        # Check request
        response = self.put('/restaurateurs/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le code postal doit être une chaine de caractère.'

    def test_invalid_city(self):
        """ PUT /restaurateurs/id: with invalid city """

        # Prepare data
        data = dict()
        data['city'] = 1111

        # Check request
        response = self.put('/restaurateurs/5', data=data)
        assert response.status_code == 400
        assert response.data == 'La ville doit être une chaine de caractère.'

    def test_invalid_language(self):
        """ PUT /restaurateurs/id: with invalid language """

        # Prepare data
        data = dict()
        data['language'] = 1111

        # Check request
        response = self.put('/restaurateurs/5', data=data)
        assert response.status_code == 400
        assert response.data == 'La langue doit être une chaine de caractère.'

    def test_invalid_country(self):
        """ PUT /restaurateurs/id: with invalid country """

        # Prepare data
        data = dict()
        data['country_id'] = "1111aaa"

        # Check request
        response = self.put('/restaurateurs/5', data=data)
        assert response.status_code == 400
        assert response.data == 'country_id doit être un identifiant.'

    def test_invalid_password(self):
        """ PUT /restaurateurs/id: with invalid password """

        # Prepare data
        data = dict()
        data['password'] = 1111

        # Check request
        response = self.put('/restaurateurs/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le mot de passe doit être une chaine de caractère.'


class Update(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        c1 = build_country(id=1, name="Canada")

        # Test 1
        build_restaurateur(id=5)

        # Test 2
        build_restaurateur(id=6)
        build_restaurant(id=2)

        # Test
        r7 = build_restaurateur(id=7)
        r8 = build_restaurateur(id=8)
        build_restaurant(id=3, restaurateur=r8)

        # Test without country
        r9 = build_restaurateur(id=9, country=c1)

        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurateurs()
        db.session.commit()

    def test_update(self):
        """ PUT /restaurateurs/id: with valid data """

        # Prepare data
        data = dict()
        data['firstname'] = "Bob"
        data['lastname'] = "Toto"
        data['birthdate'] = "2012-09-03T00:00:00.000Z"
        data['phone'] = "438-333-3333"
        data['address'] = "1000 Place Marcelle Ferron"
        data['zipcode'] = "T3R 1R1"
        data['city'] = "Trois-Rivieres"
        data['language'] = "en"
        data['country_id'] = 1
        data['password'] = "aze123"

        # Check request
        response = self.put('/restaurateurs/5', data=data)
        assert response.status_code == 200

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        restaurateur = db.session.query(Restaurateur).get(result['id'])
        assert restaurateur.firstname == "Bob"
        assert restaurateur.lastname == "Toto"
        assert restaurateur.phone == "438-333-3333"
        assert restaurateur.address == "1000 Place Marcelle Ferron"
        assert restaurateur.zipcode == "T3R 1R1"
        assert restaurateur.city == "Trois-Rivieres"
        assert restaurateur.language == "en"
        assert restaurateur.country.name == "Canada"
        assert restaurateur.password == "aze123"

    def test_update_with_restaurant(self):
        """ PUT /restaurateurs/id: with valid data """

        # Prepare data
        data = dict()
        data['restaurant_id'] = 2

        # Check request
        response = self.put('/restaurateurs/6', data=data)
        assert response.status_code == 200

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        restaurateur = db.session.query(Restaurateur).get(result['id'])
        assert restaurateur.restaurant.id == 2

    def test_update_with_restaurant_already_assigned(self):
        """ PUT /restaurateurs/id: with valid data """

        # Prepare data
        data = dict()
        data['restaurant_id'] = 3

        # Check request
        response = self.put('/restaurateurs/7', data=data)
        assert response.status_code == 400
        assert response.data == 'Le restaurant est déjà assigné à un restaurateur.'