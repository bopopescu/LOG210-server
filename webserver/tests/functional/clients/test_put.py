# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Client
from webserver.tests import build_client, build_country
from webserver.tests import delete_clients, delete_countries
from webserver.tests.functional import FunctionalTest

import datetime


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_client(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        db.session.commit()

    def test_exists(self):
        """ PUT /clients/id: exists """

        # Check request
        response = self.put('/clients/5')
        assert response.status_code != 404
        assert response.status_code != 500


class UnknownParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_client(id=15)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        db.session.commit()

    def test_unkown_id(self):
        """ PUT /clients/id: with unkown id """

        # Check request
        response = self.put('/clients/5')
        assert response.status_code == 404
        assert response.data == 'Le client n\'existe pas.'

    def test_unkown_country(self):
        """ PUT /clients/id: with unkown country_id """

        # Prepare data
        data = dict()
        data['country_id'] = 1111

        # Check request
        response = self.put('/clients/15', data=data)
        assert response.status_code == 404
        assert response.data == 'Le pays n\'existe pas.'


class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_client(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        db.session.commit()

    def test_invalid_firstname(self):
        """ PUT /clients/id: with invalid firstname """

        # Prepare data
        data = dict()
        data['firstname'] = 1111

        # Check request
        response = self.put('/clients/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom doit être une chaine de caractère.'

    def test_invalid_lastname(self):
        """ PUT /clients/id: with invalid lastname """

        # Prepare data
        data = dict()
        data['lastname'] = 1111

        # Check request
        response = self.put('/clients/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le prénom doit être une chaine de caractère.'

    def test_invalid_birthdate(self):
        """ PUT /clients/id: with invalid birthdate """

        # Prepare data
        data = dict()
        data['birthdate'] = 89382

        # Check request
        response = self.put('/clients/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le format de la date est invalide.'

    def test_invalid_phone(self):
        """ PUT /clients/id: with invalid phone """

        # Prepare data
        data = dict()
        data['phone'] = 1111

        # Check request
        response = self.put('/clients/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le numéro de téléphone doit être une chaine de caractère.'

    def test_invalid_address(self):
        """ PUT /clients/id: with invalid address """

        # Prepare data
        data = dict()
        data['address'] = 1111

        # Check request
        response = self.put('/clients/5', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse doit être une chaine de caractère.'

    def test_invalid_zipcode(self):
        """ PUT /clients/id: with invalid zipcode """

        # Prepare data
        data = dict()
        data['zipcode'] = 1111

        # Check request
        response = self.put('/clients/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le code postal doit être une chaine de caractère.'

    def test_invalid_city(self):
        """ PUT /clients/id: with invalid city """

        # Prepare data
        data = dict()
        data['city'] = 1111

        # Check request
        response = self.put('/clients/5', data=data)
        assert response.status_code == 400
        assert response.data == 'La ville doit être une chaine de caractère.'

    def test_invalid_country(self):
        """ PUT /clients/id: with invalid country """

        # Prepare data
        data = dict()
        data['country_id'] = "1111aaa"

        # Check request
        response = self.put('/clients/5', data=data)
        assert response.status_code == 400
        assert response.data == 'country_id doit être un identifiant.'

    def test_invalid_password(self):
        """ PUT /clients/id: with invalid password """

        # Prepare data
        data = dict()
        data['password'] = 1111

        # Check request
        response = self.put('/clients/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le mot de passe doit être une chaine de caractère.'


class Update(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        c1 = build_country(id=1, name="Canada")
        build_client(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        delete_countries()
        db.session.commit()

    def test_update(self):
        """ PUT /clients/id: with valid data """

        # Prepare data
        data = dict()
        data['firstname'] = "Bob"
        data['lastname'] = "Toto"
        data['birthdate'] = "2012-09-03T00:00:00.000Z"
        data['phone'] = "438-333-3333"
        data['address'] = "1000 Place Marcelle Ferron"
        data['zipcode'] = "T3R 1R1"
        data['city'] = "Trois-Rivieres"
        data['country_id'] = 1
        data['password'] = "aze123"

        # Check request
        response = self.put('/clients/5', data=data)
        assert response.status_code == 200

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        client = db.session.query(Client).get(result['id'])
        assert client.firstname == "Bob"
        assert client.lastname == "Toto"
        assert client.birthdate == datetime.date(2012, 9, 3)
        assert client.phone == "438-333-3333"
        assert client.address == "1000 Place Marcelle Ferron"
        assert client.zipcode == "T3R 1R1"
        assert client.city == "Trois-Rivieres"
        assert client.country.name == "Canada"
        assert client.password == "aze123"
