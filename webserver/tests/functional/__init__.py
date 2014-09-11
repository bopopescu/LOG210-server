import unittest
import json

from webserver import app
app = app.test_client()

class FunctionalTest(unittest.TestCase):

    def parse(self, response_data):
        """ Try to load JSON. Returns None if no JSON can be decoded """

        try:
            data = json.loads(response_data)
        except ValueError:
            log.debug('No JSON object could be decoded : %s', response_data)
            data = None

        return data

    def __open(self, url, method, user=None, data=None):
        """ Open a HTTP Request for testing """

        params = dict()
        params['method'] = method

        if data is not None:
            params['data'] = json.dumps(data)
            params['content_type'] = "application/json"

        return app.open(url, **params)

    def get(self, url):
        """ Creates a GET Request """
        return self.__open(url, 'GET')

    def post(self, url, data=None, user=None):
        """ Creates a POST request """
        return self.__open(url, 'POST', user, data)

    def put(self, url, data=None, user=None):
        """ Creates a PUT request """
        return self.__open(url, 'PUT', user, data)

    def delete(self, url, user=None):
        """ Creates a DELETE request """
        return self.__open(url, 'DELETE', user)
