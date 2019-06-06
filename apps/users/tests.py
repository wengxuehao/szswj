from io import BytesIO # 转化文件用
import json

from django.test import TestCase, RequestFactory, Client, TransactionTestCase
from django.contrib.auth.models import AnonymousUser

from .models import User
from .views import LoginView


class UserTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test120', password='admin1230', email='htzs@qq.com')

    def test_can_register(self):
        data = {
            'username': 'test120',
            'password': 'admin1230'
        }
        request = self.factory.post('/users/login/', data=data)
        request.user = self.user
        # request.user = AnonymousUser()
        response = LoginView.as_view()(request)
        response = str(response.content, encoding='utf8')
        response = json.loads(response)
        self.assertEqual(response['code'], 200, msg='登录错误1')


class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='test1', password='admin', email='htzs@qq.com')
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
    def test_login(self):
        # response = self.client.post('/users/login/', {'username': 'test1', 'password': 'admin'})
        response = self.client.force_login('test1')
        self.assertEqual(response.status_code, 200, msg='请求错误')