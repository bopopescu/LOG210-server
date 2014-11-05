# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Address
from webserver.tests import build_address, build_country
from webserver.tests import delete_addresses, delete_countries
from webserver.tests.functional import FunctionalTest

import datetime


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_address(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_addresses()
        db.session.commit()

    def test_exists(self):
        """ PUT /addresses/id: exists """

        # Check request
        response = self.put('/addresses/5')
        assert response.status_code != 404
        assert response.status_code != 500


class UnknownParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_address(id=15)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_addresses()
        db.session.commit()

    def test_unkown_id(self):
        """ PUT /addresses/id: with unkown id """

        # Check request
        response = self.put('/addresses/5')
        assert response.status_code == 404
        assert response.data == "L'adresse n'existe pas."

    def test_unkown_country(self):
        """ PUT /addresses/id: with unkown country_id """

        # Prepare data
        data = dict()
        data['country_id'] = 1111

        # Check request
        response = self.put('/addresses/15', data=data)
        assert response.status_code == 404
        assert response.data == 'Le pays n\'existe pas.'


class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_address(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_addresses()
        db.session.commit()

    def test_invalid_address(self):
        """ PUT /addresses/id: with invalid address """

        # Prepare data
        data = dict()
        data['address'] = 1111

        # Check request
        response = self.put('/addresses/5', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse doit être une chaine de caractère.'

    def test_invalid_zipcode(self):
        """ PUT /addresses/id: with invalid zipcode """

        # Prepare data
        data = dict()
        data['zipcode'] = 1111

        # Check request
        response = self.put('/addresses/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le code postal doit être une chaine de caractère.'

    def test_invalid_city(self):
        """ PUT /addresses/id: with invalid city """

        # Prepare data
        data = dict()
        data['city'] = 1111

        # Check request
        response = self.put('/addresses/5', data=data)
        assert response.status_code == 400
        assert response.data == 'La ville doit être une chaine de caractère.'

    def test_invalid_country(self):
        """ PUT /addresses/id: with invalid country """

        # Prepare data
        data = dict()
        data['country_id'] = "1111aaa"

        # Check request
        response = self.put('/addresses/5', data=data)
        assert response.status_code == 400
        assert response.data == 'country_id doit être un identifiant.'


class Update(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        c1 = build_country(id=1, name="Canada")
        build_address(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_addresses()
        delete_countries()
        db.session.commit()

    def test_update(self):
        """ PUT /addresses/id: with valid data """

        # Prepare data
        data = dict()
        data['address'] = "1000 Place Marcelle Ferron"
        data['zipcode'] = "T3R 1R1"
        data['city'] = "Trois-Rivieres"
        data['country_id'] = 1

        # Check request
        response = self.put('/addresses/5', data=data)
        assert response.status_code == 200

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        address = db.session.query(Address).get(result['id'])
        assert address.address == "1000 Place Marcelle Ferron"
        assert address.zipcode == "T3R 1R1"
        assert address.city == "Trois-Rivieres"
        assert address.country.name == "Canada"
