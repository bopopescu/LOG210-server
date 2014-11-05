# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import LineOrder, Order
from webserver.tests import build_order, build_line_order, build_dish
from webserver.tests import delete_orders, delete_lines_order, delete_dishes
from webserver.tests.functional import FunctionalTest


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_order(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_orders()
        db.session.commit()

    def test_exists(self):
        """ DELETE /orders/id: exists """

        # Check request
        response = self.delete('/orders/5')
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
        """ DELETE /orders/id: with unkown id """

        # Check request
        response = self.delete('/orders/5')
        assert response.status_code == 404
        assert response.data == "La commande n'existe pas."


class Delete(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_order(id=5)
        build_order(id=10)

        build_line_order(id=20, order_id=10)
        build_line_order(id=21, order_id=10)
        
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """
    
        delete_orders()
        delete_lines_order()
        
        db.session.commit()

    def test_delete(self):
        """ DELETE /orders/id: with valid data """

        # Check request
        response = self.delete('/orders/5')
        assert response.status_code == 200

        # Check response
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        order = db.session.query(Order).get(result['id'])
        assert order is None

    def test_delete_with_dishes(self):
        """ DELETE /orders/id: with dishes """

        # Check request
        response = self.delete('/orders/10')
        assert response.status_code == 200

        # Check response
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        order = db.session.query(Order).get(result['id'])
        assert order is None

        lo1 = db.session.query(LineOrder).get(20)
        assert lo1 is None

        lo2 = db.session.query(LineOrder).get(21)
        assert lo2 is None