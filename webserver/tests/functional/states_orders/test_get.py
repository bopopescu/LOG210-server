# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Entrepreneur
from webserver.tests import build_state_order
from webserver.tests import delete_states_orders
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
        """ GET /orders/states/id: exists """

        # Check request
        response = self.get('/orders/states/1')
        assert response.status_code != 404
        assert response.status_code != 500


class UnknownParameters(FunctionalTest):
    """  Check unknown parameters """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_unknown_id(self):
        """ GET /orders/states/id: with unknown id """

        # Check request
        response = self.get('/orders/states/666')
        assert response.status_code == 400
        assert response.data == "L'état n'existe pas."


class Get(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_state_order(id=1)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_states_orders()
        db.session.commit()

    def test_get(self):
        """ GET /orders/states/id: with valid data """

        # Check request
        response = self.get('/orders/states/1')
        assert response.status_code == 200

        # Check result
        result = self.parse(response.data)
        assert result is not None

        # Check id
        assert result['id'] == 1