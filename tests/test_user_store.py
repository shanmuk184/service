from api.stores.user import User

from tornado.testing import AsyncHTTPTestCase
from app import MyApplication
from tornado.testing import AsyncHTTPClient
from tornado.httputil import HTTPServerRequest

class TestServiceApp(AsyncHTTPTestCase):
    def get_app(self):
        application = MyApplication()
        return application.make_app()

    def test_register(self):
        testDict = {
            'name':'loki',
            'phone':'killll',
            'email':'saerty@34',
            'password':'donega'
        }
        client = AsyncHTTPClient()
        client.fetch()
