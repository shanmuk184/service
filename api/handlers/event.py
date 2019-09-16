from tornado.gen import *
from .baseHandler import BaseHandler
from api.models.group import GroupModel
from api.models.event import EventModel
import json
from tornado import web

class EventHandler(BaseHandler):
    @coroutine
    def post(self):
        user = yield self.current_user
        model = EventModel(user, self.db)
        try:
            yield model.create_event(self.args)
        except Exception as e:
            print(str(e))
        self.finish(json.dumps({'status':'success'}))