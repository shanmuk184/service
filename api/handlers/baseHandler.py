from tornado.web import RequestHandler
from tornado.gen import *
from ..models.user import UserModel
import simplejson as json
import jwt

class BaseHandler(RequestHandler):
    def __init__(self, application , request, **kwargs):
        super().__init__(application, request, **kwargs)
        self._uh = UserModel(self.get_current_user(), self.settings['db'])

    @coroutine
    def create_auth_token(self, id):
        jwt_token = jwt.encode({"id": str(id)}, key=self.settings.get('cookie_secret'), algorithm='HS256')
        raise Return(jwt_token)

    @coroutine
    def validate_auth_token(self, authToken):
        payload = jwt.decode(authToken, key=self.settings.get('cookie_secret'), algorithms='HS256')
        raise Return(payload)

    def jwt_auth(self):
        auth = self.request.headers.get('Authorization')
        options = {
            'verify_signature': True,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
        }

        if auth:
            parts = auth.split()
            if parts[0].lower() != 'bearer':
                self._transforms = []
                self.set_status(401)
                self.write("invalid header authorization")
                self.finish()
            elif len(parts) == 1:
                self._transforms = []
                self.set_status(401)
                self.write("invalid header authorization")
                self.finish()
            elif len(parts) > 2:
                self._transforms = []
                self.set_status(401)
                self.write("invalid header authorization")
                self.finish()

            token = parts[1]
            try:
                jwt.decode(
                    token,
                    self.settings['cookie_secret'],
                    options=options
                )

            except Exception as e:
                self._transforms = []
                self.set_status(401)
                self.write(e.message)
                self.finish()
        else:
            self._transforms = []
            self.write("Missing authorization")
            self.finish()
        return True

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
        auth_token = yield self.create_auth_token(user_profile.UserId)
        raise Return(auth_token)
