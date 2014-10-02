from webserver.tests import build_personne
from webserver.tests import delete_personnes
from webserver.tests.functional import FunctionalTest


class Todict(FunctionalTest):
    """ Check with valid data """

    def test_to_dict(self):
        """ Personne.to_dict """

        # Check request
        p = build_personne(id=1, firstname="Toto", lastname="Bob", phone="444-444-4444", address="1010 Avenue de la banquise", zipcode="H1S1R1", city="Montreal", mail="boby@resto.ca", password="azerty", country=None)
        response = p.to_dict()
        
        assert "id" in response
        assert response["id"] == 1
        
        assert "firstname" in response
        assert response["firstname"] == "Toto"
        
        assert "lastname" in response
        assert response["lastname"] == "Bob"
        
        assert "phone" in response
        assert response["phone"] == "444-444-4444"
        
        assert "address" in response
        assert response["address"] == "1010 Avenue de la banquise"
        
        assert "zipcode" in response
        assert response["zipcode"] == "H1S1R1"
        
        assert "city" in response
        assert response["city"] == "Montreal"
        
        assert "mail" in response
        assert response["mail"] == "boby@resto.ca"
        
        assert "password" in response
        assert response["password"] == "azerty"
        
        assert "country" not in response
        assert "country_id" not in response