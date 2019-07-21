from tornado.web import RequestHandler
from tornado.gen import *
from ..models.user import UserModel
import simplejson as json

class BaseHandler(RequestHandler):
    def __init__(self, application , request, **kwargs):
        super().__init__(application, request, **kwargs)
        self._uh = UserModel(self.get_current_user(), self.settings['db'])


    def get_current_user(self):
        pass

    def prepare(self):
        self.args = json.loads(self.request.body)

    @coroutine
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "localhost")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @coroutine
    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    @coroutine
    def set_authentication_headers(self, authToken):
        self.set_header('Authorization', 'Bearer {}'.format(authToken))

    @coroutine
    def authorize(self, user_profile):
        self.set_secure_cookie('user', user_profile.primary_email)
        auth_token = yield self._uh.create_auth_token(user_profile._id)
        raise Return(auth_token)
