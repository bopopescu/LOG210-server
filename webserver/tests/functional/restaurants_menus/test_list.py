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

        build_restaurant(id=1)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        db.session.commit()

    def test_exists(self):
        """ GET /restaurants/id/menus: exists """

        # Check request
        response = self.get('/restaurants/1/menus')
        assert response.status_code != 404
        assert response.status_code != 500


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

    def test_unkown_id(self):
        """ PUT /restaurants/id/menus: with unkown id """

        # Check request
        response = self.get('/restaurants/5/menus')
        assert response.status_code == 404
        assert response.data == "Le restaurant n'existe pas."
        
        
class Empty(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurant(id=2)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        db.session.commit()

    def test_empty(self):
        """ GET /restaurants/id/menus: empty """

        # Check request
        response = self.get('/restaurants/2/menus')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 0


class List(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurant(id=10)
        build_menu(id=1, restaurant_id=10)
        build_menu(id=2, restaurant_id=10)
        build_menu(id=4)
        build_menu(id=8, restaurant_id=10)
        
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_menus()
        delete_restaurants()
        
        db.session.commit()

    def test_list(self):
        """ GET /restaurants/id/menus: list """

        # Check request
        response = self.get('/restaurants/10/menus')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 3

        # Check id
        result_id = [r['id'] for r in result]
        assert 1 in result_id
        assert 2 in result_id
        assert 8 in result_id