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

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_exists(self):
        """ GET /restaurants/id: exists """

        # Check request
        response = self.get('/restaurants/1')
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
        """ GET /restaurants/id: with unknown id """

        # Check request
        response = self.get('/restaurants/666')
        assert response.status_code == 400
        assert response.data == 'Le restaurant n\'existe pas.'


class Get(FunctionalTest):
    """ Check with valid data """

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

    def test_get(self):
        """ GET /restaurants/id: with valid data """

        # Check request
        response = self.get('/restaurants/1')
        assert response.status_code == 200

        # Check result
        result = self.parse(response.data)
        assert result is not None

        # Check id
        assert result['id'] == 1