from tornado import web
from tornado.gen import *
from .baseHandler import BaseHandler, BaseApiHandler
import simplejson as json
from api.models.user import UserModel
from bson.json_util import dumps
from tornado_swirl.swagger import schema, restapi

@restapi('/api/register')
class RegisterHandler(BaseHandler):

    @coroutine
    def post(self):
        """Handles registration of user
            Handles native user signup and sends authToken back in the
            response

            Request Body:
                user (RegisterRequestParams) -- RegisterRequestParams data.

            200 Response:
                status (SuccessResponse) -- success
                authToken ([jwt]) -- jwtToken
            Error Responses:
                400 () -- Bad Request
                500 () -- Internal Server Error
        """
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

@restapi('/api/login')
class LoginHandler(BaseHandler):

    @coroutine
    def post(self):
        """Handles registration of user
                Handles native user signup and sends authToken back in the
                response

                Request Body:
                    user (LoginRequestParams) -- LoginRequestParams data.

                200 Response:
                    status (SuccessResponse) -- success
                    authToken ([jwt]) -- jwtToken
                Error Responses:
                    400 () -- Bad Request
                    500 () -- Internal Server Error
            """
        model = UserModel(db=self.db)
        (status, _) = yield model.login(self.args)
        if status:
            authToken = yield self.authorize(_)
            self.write(json.dumps({'status': 'success', 'auth_token': authToken}))
        else:
            self.set_status(400)
            self.write(json.dumps(_))
            self.finish()

@restapi('/api/profile')
class ProfileHandler(BaseApiHandler):
    @web.authenticated
    @coroutine
    def get(self):
        """
        Returns user Profile

        HTTP Header:
            Authorization (str) -- Required

        200 Response:
            status (ProfileSchema) -- success
        :return:
        """

        model = UserModel(user=self._user,db=self.db)
        profile = model.get_profile()

        self.write(dumps(profile))