# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Address
from webserver.tests import build_address, build_country, build_client
from webserver.tests import delete_addresses, delete_countries, delete_clients
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
        """ POST /addresses: exists """

        # Check request
        response = self.post('/addresses')
        assert response.status_code != 404
        assert response.status_code != 500


class MissingParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        country = build_country(id=1)
        build_client(id=1, country=country)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        delete_countries()
        db.session.commit()

    def test_missing_address(self):
        """ POST /addresses: with missing address """

        # Prepare data
        data = dict()
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['personne_id'] = 1

        # Check request
        response = self.post('/addresses', data=data)
        assert response.status_code == 400
        assert response.data == "L'adresse est obligatoire."

    def test_missing_zipcode(self):
        """ POST /addresses: with missing zipcode """

        # Prepare data
        data = dict()
        data['address'] = "1111 Rue des banquise"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['personne_id'] = 1

        # Check request
        response = self.post('/addresses', data=data)
        assert response.status_code == 400
        assert response.data == "Le code postal est obligatoire."

    def test_missing_city(self):
        """ POST /addresses: with missing city """

        # Prepare data
        data = dict()
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['country_id'] = 1
        data['personne_id'] = 1

        # Check request
        response = self.post('/addresses', data=data)
        assert response.status_code == 400
        assert response.data == "La ville est obligatoire."

    def test_missing_country(self):
        """ POST /addresses: with missing country """

        # Prepare data
        data = dict()
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['personne_id'] = 1

        # Check request
        response = self.post('/addresses', data=data)
        assert response.status_code == 400
        assert response.data == "Le pays est obligatoire."
        
    def test_missing_personne(self):
        """ POST /addresses: with missing personne """

        # Prepare data
        data = dict()
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1

        # Check request
        response = self.post('/addresses', data=data)
        assert response.status_code == 400
        assert response.data == "L'identifiant d'une personne est obligatoire."


class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        country = build_country(id=1, name="Canada")
        build_client(id=12, country=country)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        delete_countries()
        db.session.commit()

    def test_invalid_address(self):
        """ POST /addresses: with invalid address """

        # Prepare data
        data = dict()
        data['address'] = 11
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['personne_id'] = 12

        # Check request
        response = self.post('/addresses', data=data)
        assert response.status_code == 400
        print response.data
        assert response.data == "L'adresse doit être une chaine de caractère."

    def test_invalid_zipcode(self):
        """ POST /addresses: with invalid zipcode """

        # Prepare data
        data = dict()
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = 11
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['personne_id'] = 12

        # Check request
        response = self.post('/addresses', data=data)
        assert response.status_code == 400
        assert response.data == "Le code postal doit être une chaine de caractère."

    def test_invalid_city(self):
        """ POST /addresses: with invalid city """

        # Prepare data
        data = dict()
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = 2192901
        data['country_id'] = 1
        data['personne_id'] = 12

        # Check request
        response = self.post('/addresses', data=data)
        assert response.status_code == 400
        assert response.data == "La ville doit être une chaine de caractère."

    def test_invalid_country(self):
        """ POST /addresses: with invalid country """

        # Prepare data
        data = dict()
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = "ae1"
        data['personne_id'] = 12

        # Check request
        response = self.post('/addresses', data=data)
        assert response.status_code == 400
        assert response.data == "country_id doit être un identifiant."
        
    def test_invalid_personne(self):
        """ POST /addresses: with invalid personne """

        # Prepare data
        data = dict()
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = "ae1"
        data['personne_id'] = "ahaha"

        # Check request
        response = self.post('/addresses', data=data)
        assert response.status_code == 400
        assert response.data == "personne_id doit être un identifiant."


class UnknownParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_country(id=3)
        build_client(id=15)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        delete_countries()
        db.session.commit()

    def test_unknown_country(self):
        """ POST /addresses: with invalid country """

        # Prepare data
        data = dict()
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 999
        data['personne_id'] = 15

        # Check request
        response = self.post('/addresses', data=data)
        print response.status_code
        assert response.status_code== 404
        assert response.data == "Le pays n'existe pas."
        
    def test_unknown_personne(self):
        """ POST /addresses: with invalid personne """

        # Prepare data
        data = dict()
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 3
        data['personne_id'] = 666

        # Check request
        response = self.post('/addresses', data=data)
        print response.status_code
        assert response.status_code== 404
        assert response.data == "La personne n'existe pas."


class Create(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_country(id=1, name="Canada")
        build_client(id=20)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        delete_addresses()
        delete_countries()
        db.session.commit()

    def test_create(self):
        """ POST /addresses: with valid data """

        # Prepare data
        data = dict()
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['personne_id'] = 20

        # Check request
        response = self.post('/addresses', data=data)
        assert response.status_code == 201

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        address = db.session.query(Address).get(result['id'])
        assert address is not None
