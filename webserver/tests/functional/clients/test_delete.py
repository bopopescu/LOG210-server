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

        build_client(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        db.session.commit()

    def test_exists(self):
        """ DELETE /clients/id: exists """

        # Check request
        response = self.delete('/clients/5')
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
        """ DELETE /clients/id: with unkown id """

        # Check request
        response = self.delete('/clients/5')
        assert response.status_code == 404
        assert response.data == 'Le client n\'existe pas.'


class Delete(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_client(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_clients()
        db.session.commit()

    def test_delete(self):
        """ DELETE /clients/id: with valid data """

        # Check request
        response = self.delete('/clients/5')
        assert response.status_code == 200

        # Check response
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        client = db.session.query(Client).get(result['id'])
        assert client is None