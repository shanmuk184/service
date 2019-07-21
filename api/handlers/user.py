from tornado import web
from tornado.gen import *
from .baseHandler import BaseHandler
import simplejson as json

class RegisterHandler(BaseHandler):
    @coroutine
    def post(self):
        response = yield self._uh.create_user(self.args)
        self.write(json.dumps(response))


class LoginHandler(BaseHandler):

    @coroutine
    def post(self):
        user = yield self._uh.login(self.args)
        if user.get('userProfile'):
            authToken = yield self.authorize(user.get('userProfile'))
            self.write(json.dumps({'status': 'success', 'auth_token': authToken}))
        else:
            self.write(json.dumps(user))
