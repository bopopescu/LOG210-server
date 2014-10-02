from webserver import db
from webserver.models import Restaurateur
from webserver.tests import build_restaurateur, build_country
from webserver.tests import delete_restaurateurs, delete_countries
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
        """ POST /restaurateurs: exists """

        # Check request
        response = self.post('/restaurateurs')
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

    def test_missing_firstname(self):
        """ POST /restaurateurs: with missing firstname """

        # Prepare data
        data = dict()
        data['lastname'] = "Titi"
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom du restaurateur est obligatoire.'

    def test_missing_lastname(self):
        """ POST /restaurateurs: with missing lastname """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le prenom du restaurateur est obligatoire.'

    def test_missing_mail(self):
        """ POST /restaurateurs: with missing firstname """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['password'] = "azerty"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse mail du restaurateur est obligatoire.'

    def test_missing_password(self):
        """ POST /restaurateurs: with missing password """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['mail'] = "titi@toto.ca"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le mot de passe du restaurateur est obligatoire.'


class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurateur(id=10, mail="bob@bob.ti")
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurateurs()
        db.session.commit()

    def test_invalid_firstname(self):
        """ POST /restaurateurs: with invalid firstname """

        # Prepare data
        data = dict()
        data['firstname'] = 19090
        data['lastname'] = "Titi"
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom du restaurateur doit etre une chaine de caractere.'


    def test_invalid_lastname(self):
        """ POST /restaurateurs: with invalid lastname """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = 30923
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le prenom du restaurateur doit etre une chaine de caractere.'

    def test_invalid_phone(self):
        """ POST /restaurateurs: with invalid phone """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['phone'] = 948923
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le numero de telephone du restaurateur doit etre une chaine de caractere.'

    def test_invalid_address(self):
        """ POST /restaurateurs: with invalid address """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['address'] = 1111
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse du restaurateur doit etre une chaine de caractere.'

    def test_invalid_zipcode(self):
        """ POST /restaurateurs: with invalid zipcode """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['zipcode'] = 11111
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le code postal du restaurateur doit etre une chaine de caractere.'

    def test_invalid_city(self):
        """ POST /restaurateurs: with invalid city """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['city'] = 11111
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'La ville du restaurateur doit etre une chaine de caractere.'

    def test_invalid_country(self):
        """ POST /restaurateurs: with invalid country """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['country_id'] = "11111aaa"
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'country_id doit etre un identifiant.'

    def test_invalid_mail(self):
        """ POST /restaurateurs: with invalid mail """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['mail'] = 11111
        data['password'] = "azerty"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse mail du restaurateur doit etre une chaine de caractere.'

    def test_invalid_password(self):
        """ POST /restaurateurs: with invalid password """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['mail'] = "titi@toto.ca"
        data['password'] = 1010101

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 400
        assert response.data == 'Le mot de passe du restaurateur doit etre une chaine de caractere.'

    def test_invalid_mail_already_used(self):
        """ POST /restaurateurs: with mail already used """

        # Prepare data
        data = dict()
        data['firstname'] = "Toto"
        data['lastname'] = "Titi"
        data['mail'] = "bob@bob.ti"
        data['password'] = "1010101"

        # Check request
        response = self.post('/restaurateurs', data=data)
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
        """ POST /restaurateurs: with invalid country """

        # Prepare data
        data = dict()
        data['firstname'] = "Titi"
        data['lastname'] = "Toto"
        data['mail'] = "titi@toto.ca"
        data['password'] = "azerty123"
        data['country_id'] = 999

        # Check request
        response = self.post('/restaurateurs', data=data)
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

        delete_restaurateurs()
        delete_countries()
        db.session.commit()

    def test_create(self):
        """ POST /restaurateurs: with valid data """

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
        data['password'] = "azerty123"

        # Check request
        response = self.post('/restaurateurs', data=data)
        assert response.status_code == 201

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        restaurateur = db.session.query(Restaurateur).get(result['id'])
        assert restaurateur is not None