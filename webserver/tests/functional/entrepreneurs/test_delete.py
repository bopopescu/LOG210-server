from webserver import db
from webserver.models import Entrepreneur
from webserver.tests import build_entrepreneur
from webserver.tests import delete_entrepreneurs
from webserver.tests.functional import FunctionalTest


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_entrepreneur(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_entrepreneurs()
        db.session.commit()

    def test_exists(self):
        """ DELETE /entrepreneurs/id: exists """

        # Check request
        response = self.delete('/entrepreneurs/5')
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
        """ DELETE /entrepreneurs/id: with unkown id """

        # Check request
        response = self.delete('/entrepreneurs/5')
        assert response.status_code == 404
        assert response.data == 'Le entrepreneur n\'existe pas.'


class Delete(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_entrepreneur(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_entrepreneurs()
        db.session.commit()

    def test_delete(self):
        """ DELETE /entrepreneurs/id: with valid data """

        # Check request
        response = self.delete('/entrepreneurs/5')
        assert response.status_code == 200

        # Check response
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        entrepreneur = db.session.query(Entrepreneur).get(result['id'])
        assert entrepreneur is None