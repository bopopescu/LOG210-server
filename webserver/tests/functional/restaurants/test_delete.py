# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Restaurant
from webserver.tests import build_restaurant
from webserver.tests import delete_restaurants
from webserver.tests.functional import FunctionalTest


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurant(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        db.session.commit()

    def test_exists(self):
        """ DELETE /restaurants/id: exists """

        # Check request
        response = self.delete('/restaurants/5')
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
        """ DELETE /restaurants/id: with unkown id """

        # Check request
        response = self.delete('/restaurants/5')
        assert response.status_code == 404
        assert response.data == 'Le restaurant n\'existe pas.'


class Delete(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurant(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        db.session.commit()

    def test_delete(self):
        """ DELETE /restaurants/id: with valid data """

        # Check request
        response = self.delete('/restaurants/5')
        assert response.status_code == 200

        # Check response
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        restaurant = db.session.query(Restaurant).get(result['id'])
        assert restaurant is None
