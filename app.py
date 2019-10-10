import tornado.ioloop
import tornado.web
from urls import urlpatterns
from db.db import Database
from config.config import Settings
from tornado_swirl.swagger import Application, describe
from tornado_swirl import api_routes
from tornado.options import define, options

settings = Settings()

describe(title='UMS API', description='Manages User Operations')
define('mongo_host', default='127.0.0.1:')


class MyApplication(object):
    def __init__(self):
        self.database = Database()
        self.initiateApp()

    def initiateApp(self):
        app = self.make_app()
        app.listen(8888)

    def make_app(self):
        db = self.database.get_motor_connection()
        return Application(api_routes(),
                                       db = db,
                                       cookie_secret=settings.CookieSecret,
                                       debug=settings.Debug,
                                       key_version=settings.KeyVersion,
                                       version=settings.Version,
                                        login_url='api/login'
                                       )

class MainHandler(tornado.web.RequestHandler):
    """This is the main handler"""
    def get(self):
        self.write("Hello, world")


if __name__ == "__main__":
    app = MyApplication()
    print("server is running on 8888")
    tornado.ioloop.IOLoop.current().start()
    io_loop = tornado.ioloop.IOLoop.instance()