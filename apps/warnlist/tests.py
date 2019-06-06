from django.test import TestCase, RequestFactory
from django.test import Client

from apps.warnlist.models import WarnModel


class SimpleTest(TestCase):
    def test_details(self):
        c = Client()
        response = self.client.post('/users/login/', {'username': 'admin', 'password': 'admin1230'}, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)
        # response = c.get('/users/login/', HTTP_USER_AGENT='Mozilla/5.0')
        # content = response.content
        # print(content)


class WarnTest(TestCase):
    def setUp(self):
        pass


