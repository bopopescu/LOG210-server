# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Livreur
from webserver.tests import build_livreur, build_country
from webserver.tests import delete_livreurs, delete_countries
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
        """ POST /livreurs: exists """

        # Check request
        response = self.post('/livreurs')
        assert response.status_code != 404
        assert response.status_code != 500


class MissingParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_country(id=1)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_countries()
        db.session.commit()

    def test_missing_firstname(self):
        """ POST /livreurs: with missing firstname """

        # Prepare data
        data = dict()
        data['lastname'] = "Titi"
        data['birthdate'] = None
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty123"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom est obligatoire.'

    def test_missing_lastname(self):
        """ POST /livreurs: with missing lastname """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty123"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le prénom est obligatoire.'

    def test_missing_phone(self):
        """ POST /livreurs: with missing phone """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty123"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le numéro de téléphone est obligatoire.'

    def test_missing_address(self):
        """ POST /livreurs: with missing address """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty123"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse est obligatoire.'

    def test_missing_zipcode(self):
        """ POST /livreurs: with missing zipcode """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty123"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le code postal est obligatoire.'

    def test_missing_city(self):
        """ POST /livreurs: with missing city """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty123"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'La ville est obligatoire.'

    def test_missing_country(self):
        """ POST /livreurs: with missing country """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty123"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le pays est obligatoire.'

    def test_missing_mail(self):
        """ POST /livreurs: with missing mail """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['password'] = "azerty123"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse mail est obligatoire.'

    def test_missing_password(self):
        """ POST /livreurs: with missing password """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le mot de passe est obligatoire.'


class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_country(id=1, name="Canada")
        build_livreur(id=10, mail="bob@bob.ti")
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_livreurs()
        delete_countries()
        db.session.commit()

    def test_invalid_firstname(self):
        """ POST /livreurs: with invalid firstname """

        # Prepare data
        data = dict()
        data['firstname'] = 12121
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom doit être une chaine de caractère.'


    def test_invalid_lastname(self):
        """ POST /livreurs: with invalid lastname """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = 89382
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le prénom doit être une chaine de caractère.'

    def test_invalid_birthdate(self):
        """ POST /livreurs: with invalid birthdate """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['birthdate'] = 89382
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        print response.data
        assert response.data == 'Le format de la date est invalide.'

    def test_invalid_phone(self):
        """ POST /livreurs: with invalid phone """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = 309032
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le numéro de téléphone doit être une chaine de caractère.'

    def test_invalid_address(self):
        """ POST /livreurs: with invalid address """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['birthdate'] = "2012-09-03T00:00:00.000Z"
        data['phone'] = "514-444-4444"
        data['address'] = 11
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        print response.data
        assert response.data == 'L\'adresse doit être une chaine de caractère.'

    def test_invalid_zipcode(self):
        """ POST /livreurs: with invalid zipcode """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = 11
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le code postal doit être une chaine de caractère.'

    def test_invalid_city(self):
        """ POST /livreurs: with invalid city """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = 2192901
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'La ville doit être une chaine de caractère.'

    def test_invalid_country(self):
        """ POST /livreurs: with invalid country """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = "ae1"
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'country_id doit être un identifiant.'

    def test_invalid_mail(self):
        """ POST /livreurs: with invalid mail """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = 1111
        data['password'] = "azerty"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse mail doit être une chaine de caractère.'

    def test_invalid_password(self):
        """ POST /livreurs: with invalid password """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = 1010

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le mot de passe doit être une chaine de caractère.'

    def test_invalid_mail_already_used(self):
        """ POST /livreurs: with mail already used """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "bob@bob.ti"
        data['password'] = "1010101"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse mail est deja utilisee par un utilisateur.'


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

    def test_unknown_country(self):
        """ POST /livreurs: with invalid country """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 999
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/livreurs', data=data)
        print response.status_code
        assert response.status_code== 404
        assert response.data == 'Le pays n\'existe pas.'


class Create(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_country(id=1, name="Canada")
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_livreurs()
        delete_countries()
        db.session.commit()

    def test_create(self):
        """ POST /livreurs: with valid data """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['birthdate'] = "2012-09-03T00:00:00.000Z"
        data['phone'] = "514-444-4444"
        data['address'] = "1111 Rue des banquise"
        data['zipcode'] = "H3A A1A"
        data['city'] = "Montreal"
        data['country_id'] = 1
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty123"

        # Check request
        response = self.post('/livreurs', data=data)
        assert response.status_code == 201

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        livreur = db.session.query(Livreur).get(result['id'])
        assert livreur is not None
