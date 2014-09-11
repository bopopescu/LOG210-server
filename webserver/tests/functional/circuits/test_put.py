# from webserver import db
# from webserver.models import Restaurant
# from webserver.tests import build_restaurant
# from webserver.tests import delete_restaurants
# from webserver.tests.functional import FunctionalTest
#
#
# class Exists(FunctionalTest):
#     """ Check if the webservice exists """
#
#     @classmethod
#     def setup_class(cls):
#         """ Add database fixtures """
#
#         build_restaurant(id=5)
#         db.session.commit()
#
#     @classmethod
#     def teardown_class(cls):
#         """ Clear database fixtures """
#
#         delete_restaurants()
#         db.session.commit()
#
#     def test_exists(self):
#         """ PUT /restaurants/id: exists """
#
#         # Check request
#         response = self.put('/restaurants/5')
#         assert response.status_code != 404
#         assert response.status_code != 500
#
#
# class UnknownParameters(FunctionalTest):
#     """ Check with no datas """
#
#     @classmethod
#     def setup_class(cls):
#         """ Add database fixtures """
#
#         pass
#
#     @classmethod
#     def teardown_class(cls):
#         """ Clear database fixtures """
#
#         pass
#
#     def test_unkown_id(self):
#         """ PUT /restaurants/id: with unkown id """
#
#         # Check request
#         response = self.put('/restaurants/5')
#         assert response.status_code == 400
#         assert response.data == 'The restaurant you are trying to target is unknown'
#
#
# class InvalidParameters(FunctionalTest):
#     """ Check with no datas """
#
#     @classmethod
#     def setup_class(cls):
#         """ Add database fixtures """
#
#         build_restaurant(id=5, name="Nurburgring", city="Koblenz", country="Germany")
#         db.session.commit()
#
#     @classmethod
#     def teardown_class(cls):
#         """ Clear database fixtures """
#
#         delete_restaurants()
#         db.session.commit()
#
#     def test_invalid_name(self):
#         """ PUT /restaurants/id: with invalid name """
#
#         # Prepare data
#         data = dict()
#         data['name'] = 1
#
#         # Check request
#         response = self.put('/restaurants/5', data=data)
#         assert response.status_code == 400
#         assert response.data == 'The name must be a string'
#
#     def test_invalid_city(self):
#         """ PUT /restaurants/id: with invalid city """
#
#         # Prepare data
#         data = dict()
#         data['city'] = 1
#
#         # Check request
#         response = self.put('/restaurants/5', data=data)
#         assert response.status_code == 400
#         assert response.data == 'The city must be a string'
#
#     def test_invalid_country(self):
#         """ PUT /restaurants/id: with invalid country """
#
#         # Prepare data
#         data = dict()
#         data['country'] = 1
#
#         # Check request
#         response = self.put('/restaurants/5', data=data)
#         assert response.status_code == 400
#         assert response.data == 'The country must be a string'
#
#
# class Update(FunctionalTest):
#     """ Check with valid data """
#
#     @classmethod
#     def setup_class(cls):
#         """ Add database fixtures """
#
#         build_restaurant(id=5, name="Nurburgring", city="Koblenz", country="Germany")
#         db.session.commit()
#
#     @classmethod
#     def teardown_class(cls):
#         """ Clear database fixtures """
#
#         delete_restaurants()
#         db.session.commit()
#
#     def test_update(self):
#         """ PUT /restaurants/id: with valid data """
#
#         # Prepare data
#         data = dict()
#         data['name'] = "Restaurant 1"
#         data['city'] = "City 1"
#         data['country'] = "Country 1"
#
#         # Check request
#         response = self.put('/restaurants/5', data=data)
#         assert response.status_code == 200
#
#         # Check received data
#         result = self.parse(response.data)
#         assert 'id' in result
#
#         # Check in database
#         restaurant = db.session.query(Restaurant).get(result['id'])
#         assert restaurant.name == 'Restaurant 1'
#         assert restaurant.city == 'City 1'
#         assert restaurant.country == 'Country 1'