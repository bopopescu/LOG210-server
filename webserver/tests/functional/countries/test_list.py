# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Entrepreneur
from webserver.tests import build_country
from webserver.tests import delete_countries
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
        """ GET /countries: exists """

        # Check request
        response = self.get('/countries')
        assert response.status_code != 404
        assert response.status_code != 500


class Empty(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_empty(self):
        """ GET /countries: empty """

        # Check request
        response = self.get('/countries')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 0


class List(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_country(id=1)
        build_country(id=2)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_countries()
        db.session.commit()

    def test_list(self):
        """ GET /countries: list """

        # Check request
        response = self.get('/countries')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 2

        # Check id
        result_id = [r['id'] for r in result]
        assert 1 in result_id
        assert 2 in result_id