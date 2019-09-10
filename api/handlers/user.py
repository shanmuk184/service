from tornado import web
from tornado.gen import *
from .baseHandler import BaseHandler
import simplejson as json
from api.models.user import UserModel
from bson.json_util import dumps

class RegisterHandler(BaseHandler):
    @coroutine
    def post(self):
        model = UserModel(db=self.db)
        try:
            (status, _) = yield model.create_user(self.args)
        except Exception as e:
            (status, _) = (False, str(e))
        if status:
            authToken = yield self.authorize(_)
            self.write(json.dumps({'status': 'success', 'auth_token': authToken}))
            self.finish()
        else:
            self.set_status(400)
            self.write(_)
            self.finish()

class LoginHandler(BaseHandler):
    @coroutine
    def post(self):
        model = UserModel(db=self.db)
        (status, _) = yield model.login(self.args)
        if status:
            authToken = yield self.authorize(_)
            self.write(json.dumps({'status': 'success', 'auth_token': authToken}))
        else:
            self.set_status(400)
            self.write(json.dumps(_))
            self.finish()

class ProfileHandler(BaseHandler):

    @web.authenticated
    @coroutine
    def get(self):
        user = yield self.current_user
        model = UserModel(user=user,db=self.db)
        profile = yield model.get_profile()
        self.write(dumps(profile))