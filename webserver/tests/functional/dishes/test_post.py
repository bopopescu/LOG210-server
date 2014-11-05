# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Dish
from webserver.tests import build_dish, build_menu
from webserver.tests import delete_dishes, delete_menus
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
        """ POST /dishes: exists """

        # Check request
        response = self.post('/dishes')
        assert response.status_code != 404
        assert response.status_code != 500


class MissingParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_menu(id=10)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_menus()
        db.session.commit()

    def test_missing_name(self):
        """ POST /dishes: with missing name """

        # Prepare data
        data = dict()
        data['description'] = "un bon burger"
        data['price'] = 111.11
        data['menu_id'] = 10

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom du plat est obligatoire.'

    def test_missing_price(self):
        """ POST /dishes: with missing price """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = "Titi"
        data['menu_id'] = 10
       
        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'Le prix du plat est obligatoire.'
        
    def test_missing_menu(self):
        """ POST /dishes: with missing menu """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = "Titi"
        data['price'] = 10
       
        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'menu_id est obligatoire.'

    
class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_menu(id=11)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_menus()
        db.session.commit()

    def test_invalid_name(self):
        """ POST /dishes: with invalid name """

        # Prepare data
        data = dict()
        data['name'] = 19090
        data['description'] = "Titi"
        data['price'] = 12.43
        data['menu_id'] = 11

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom du plat doit être une chaine de caractère.'


    def test_invalid_description(self):
        """ POST /dishes: with invalid description """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = 30923
        data['price'] = 12.43
        data['menu_id'] = 11

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'La description du plat doit être une chaine de caractère.'

    
    def test_invalid_price(self):
        """ POST /dishes: with invalid price """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = "Titi"
        data['price'] = "azerty"
        data['menu_id'] = 11

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'Le prix du plat doit être numerique.'

    def test_negative_price(self):
        """ POST /dishes: with negative price """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = "Titi"
        data['price'] = (-30)
        data['menu_id'] = 11

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'Le prix du plat doit être positif.'
        
    def test_invalid_menu(self):
        """ POST /dishes: with negative price """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = "Titi"
        data['price'] = 45
        data['menu_id'] = "ahah"

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'menu_id doit être un identifiant.'


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
        
    def test_unknown_menu(self):
        """ POST /dishes: with unknown menu """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = "Titi"
        data['price'] = 12
        data['menu_id'] = 11

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 404
        assert response.data == "Le menu n'existe pas."


class Create(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_menu(id=12)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
        delete_menus()
        db.session.commit()

    def test_create(self):
        """ POST /dishes: with valid data """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = "Titi description"
        data['price'] = 23.33
        data['menu_id'] = 12

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 201

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        dish = db.session.query(Dish).get(result['id'])
        assert dish is not None