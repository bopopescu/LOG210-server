# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Menu
from webserver.tests import build_menu, build_restaurant
from webserver.tests import delete_menus, delete_restaurants
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
        """ POST /menus: exists """

        # Check request
        response = self.post('/menus')
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

    def test_missing_restaurant_id(self):
        """ POST /menus: with missing restaurant_id """

        # Prepare data
        data = dict()
        data['name'] = "Menu du pecheur"

        # Check request
        response = self.post('/menus', data=data)
        assert response.status_code == 400
        assert response.data == "restaurant_id est obligatoire."

    
class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurant(id=10)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        db.session.commit()

    def test_invalid_name(self):
        """ POST /menus: with invalid name """

        # Prepare data
        data = dict()
        data['name'] = 19090
        data['restaurant_id'] = 10

        # Check request
        response = self.post('/menus', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom du menu doit être une chaine de caractère.'
        
    def test_invalid_restaurant_id(self):
        """ POST /menus: with invalid restaurant_id """

        # Prepare data
        data = dict()
        data['name'] = "Menu du pecheur"
        data['restaurant_id'] = "ahahah"

        # Check request
        response = self.post('/menus', data=data)
        assert response.status_code == 400
        assert response.data == "restaurant_id doit être un identifiant."


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
        
    def test_unknown_restaurant_id(self):
        """ POST /menus: with unkown restaurant_id """

        # Prepare data
        data = dict()
        data['name'] = "Menu du pecheur"
        data['restaurant_id'] = 293

        # Check request
        response = self.post('/menus', data=data)
        assert response.status_code == 404
        assert response.data == "Le restaurant n'existe pas."


class Create(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurant(id=12)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_menus()
        delete_restaurants()
        
        db.session.commit()

    def test_create(self):
        """ POST /menus: with valid data """

        # Prepare data
        data = dict()
        data['name'] = "Menu du printemps"
        data['restaurant_id'] = 12

        # Check request
        response = self.post('/menus', data=data)
        assert response.status_code == 201

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        menu = db.session.query(Menu).get(result['id'])
        assert menu is not None