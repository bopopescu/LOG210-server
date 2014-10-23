# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Dish, Menu
from webserver.tests import build_menu, build_dish
from webserver.tests import delete_menus, delete_dishes
from webserver.tests.functional import FunctionalTest


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_menu(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_menus()
        db.session.commit()

    def test_exists(self):
        """ DELETE /menus/id: exists """

        # Check request
        response = self.delete('/menus/5')
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
        """ DELETE /menus/id: with unkown id """

        # Check request
        response = self.delete('/menus/5')
        assert response.status_code == 404
        assert response.data == "Le menu n'existe pas."


class Delete(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_menu(id=5)
        
        build_menu(id=10)
        build_dish(id=20, menu_id=10)
        build_dish(id=21, menu_id=10)
        
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
        delete_menus()
        db.session.commit()

    def test_delete(self):
        """ DELETE /menus/id: with valid data """

        # Check request
        response = self.delete('/menus/5')
        assert response.status_code == 200

        # Check response
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        menu = db.session.query(Menu).get(result['id'])
        assert menu is None
        
    def test_delete_with_dishes(self):
        """ DELETE /menus/id: with dishes """

        # Check request
        response = self.delete('/menus/10')
        assert response.status_code == 200

        # Check response
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        menu = db.session.query(Menu).get(result['id'])
        assert menu is None
        
        dish = db.session.query(Dish).get(20)
        assert dish is None
        
        dish = db.session.query(Dish).get(21)
        assert dish is None