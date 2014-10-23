# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Dish
from webserver.tests import build_dish
from webserver.tests import delete_dishes
from webserver.tests.functional import FunctionalTest


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_dish(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
        db.session.commit()

    def test_exists(self):
        """ PUT /dishes/id: exists """

        # Check request
        response = self.put('/dishes/5')
        assert response.status_code != 404
        assert response.status_code != 500


class UnknownParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_dish(id=15)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
        db.session.commit()

    def test_unkown_id(self):
        """ PUT /dishes/id: with unkown id """

        # Check request
        response = self.put('/dishes/5')
        assert response.status_code == 404
        assert response.data == 'Le plat n\'existe pas.'

    
class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_dish(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
        db.session.commit()

    def test_invalid_name(self):
        """ PUT /dishes/id: with invalid name """

        # Prepare data
        data = dict()
        data['name'] = 1111

        # Check request
        response = self.put('/dishes/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom du plat doit être une chaine de caractère.'

    def test_invalid_description(self):
        """ PUT /dishes/id: with invalid description """

        # Prepare data
        data = dict()
        data['description'] = 1111

        # Check request
        response = self.put('/dishes/5', data=data)
        assert response.status_code == 400
        assert response.data == 'La description du plat doit être une chaine de caractère.'

    def test_invalid_price(self):
        """ PUT /dishes/id: with invalid price """

        # Prepare data
        data = dict()
        data['price'] = "aaaaaa"

        # Check request
        response = self.put('/dishes/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le prix du plat doit être numerique.'




class Update(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_dish(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
        db.session.commit()

    def test_update(self):
        """ PUT /dishes/id: with valid data """

        # Prepare data
        data = dict()
        data['name'] = "Pizza vege"
        data['description'] = "Une bonne grosse pizza"
        data['price'] = 12.34
   

        # Check request
        response = self.put('/dishes/5', data=data)
        assert response.status_code == 200

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        dish = db.session.query(Dish).get(result['id'])
        assert dish.name == "Pizza vege"
        assert dish.description == "Une bonne grosse pizza"
        assert dish.price == 12.34

