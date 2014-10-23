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
        """ DELETE /dishes/id: exists """

        # Check request
        response = self.delete('/dishes/5')
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
        """ DELETE /dishes/id: with unkown id """

        # Check request
        response = self.delete('/dishes/5')
        assert response.status_code == 404
        assert response.data == 'Le plat n\'existe pas.'


class Delete(FunctionalTest):
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

    def test_delete(self):
        """ DELETE /dishes/id: with valid data """

        # Check request
        response = self.delete('/dishes/5')
        assert response.status_code == 200

        # Check response
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        dish = db.session.query(Dish).get(result['id'])
        assert dish is None