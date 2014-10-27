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

        build_menu(id=1)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_menus()
        db.session.commit()

    def test_exists(self):
        """ GET /menus/id/dishes: exists """

        # Check request
        response = self.get('/menus/1/dishes')
        assert response.status_code != 404
        assert response.status_code != 500


class Empty(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_menu(id=12)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_menus()
        db.session.commit()

    def test_empty(self):
        """ GET /menus/id/dishes: empty """

        # Check request
        response = self.get('/menus/12/dishes')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 0


class List(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_menu(id=34)
        build_dish(id=1, menu_id=34)
        build_dish(id=2, menu_id=34)
        build_dish(id=3, menu_id=34)
        build_dish(id=4)    
        
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
        db.session.commit()

    def test_list(self):
        """ GET /menus/id/dishes: list """

        # Check request
        response = self.get('/menus/34/dishes')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 3

        # Check id
        result_id = [r['id'] for r in result]
        assert 1 in result_id
        assert 2 in result_id
        assert 3 in result_id