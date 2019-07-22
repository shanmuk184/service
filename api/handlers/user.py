from tornado import web
from tornado.gen import *
from .baseHandler import BaseHandler
import simplejson as json

class RegisterHandler(BaseHandler):
    @coroutine
    def post(self):
        (status, _) = yield self._uh.create_user(self.args)
        if status:
            authToken = yield self.authorize(_)
            self.write(json.dumps({'status': 'success', 'auth_token': authToken}))
        else:
            self.set_status(400)
            self.write(_)
            self.finish()

class LoginHandler(BaseHandler):
    @coroutine
    def post(self):
        (status, _) = yield self._uh.login(self.args)
        if status:
            authToken = yield self.authorize(_)
            self.write(json.dumps({'status': 'success', 'auth_token': authToken}))
        else:
            self.set_status(400)
            self.write(json.dumps(_))
            self.finish()
