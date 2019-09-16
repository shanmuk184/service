from tornado.gen import coroutine, Return
from api.stores.group import Group
from api.stores.user import SupportedRoles, User, StatusType
from db import QueryConstants
from tornado.gen import *
import bcrypt
import jwt
import base64
from api.stores.user import User, LinkedAccount, LinkedAccountType
from api.core.user import UserHelper
from api.core.group import GroupHelper
from api.core.event import EventHelper
import tornado.ioloop


class EventModel(object):
    def __init__(self, user=None, db=None):
        if not db:
            raise ValueError('db should be present')
        if user:
            self._user = user
        self.db = db
        if self.db:
            self._gh = GroupHelper(self._user, self.db)
            self._uh = UserHelper(self._user, self.db)
            self._eh = EventHelper(self._user, self.db)

    @coroutine
    def create_event(self, eventDict):
        if not eventDict:
            raise NotImplementedError()
        yield self._eh.create_event(eventDict)


        raise Return(group)

