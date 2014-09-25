from webserver import db
from webserver.models import Client
from webserver.tests import build_client
from webserver.tests import delete_clients
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
        """ GET /clients: exists """

        # Check request
        response = self.get('/clients')
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
        """ GET /clients: empty """

        # Check request
        response = self.get('/clients')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 0


class List(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_client(id=1)
        build_client(id=2)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        db.session.commit()

    def test_list(self):
        """ GET /clients: list """

        # Check request
        response = self.get('/clients')
        assert response.status_code == 200

        # Check length
        result = self.parse(response.data)
        assert len(result) == 2

        # Check id
        result_id = [r['id'] for r in result]
        assert 1 in result_id
        assert 2 in result_id