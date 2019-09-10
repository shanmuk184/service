from tornado.gen import *
from .baseHandler import BaseHandler
from api.models.group import GroupModel
import json
from tornado import web
class GroupHandler(BaseHandler):
    @web.authenticated
    @coroutine
    def post(self):
        user = yield self.current_user
        model = GroupModel(user=user, db=self.db)
        try:
            yield model.create_group(self.args)
        except Exception as e:
            pass
        raise Return(json.dumps({'status':'success'}))
