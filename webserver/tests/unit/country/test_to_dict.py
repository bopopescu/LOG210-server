from webserver.tests import build_country
from webserver.tests import delete_countries
from webserver.tests.functional import FunctionalTest


class Todict(FunctionalTest):
    """ Check with valid data """

    def test_to_dict(self):
        """ Country.to_dict """

        # Check request
        c = build_country(id=1,name='Canada')
        response = c.to_dict()
        
        assert "id" in response
        assert response["id"] == 1
        
        assert "name" in response
        assert response["name"] == "Canada"