from tornado.gen import *
from .baseHandler import BaseHandler
from api.models.group import GroupModel
import json
from tornado import web
from bson.json_util import dumps
class GroupsListHandler(BaseHandler):
    @web.authenticated
    @coroutine
    def get(self):
        model = GroupModel(user=self._user, db=self.db)
        (status, _) = yield model.get_groups_for_user(self._user.UserId)
        if status:
            self.finish(dumps(_))
        else:
            self.set_status(400, _)
            self.finish()

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
        self.finish(json.dumps({'status':'success'}))


