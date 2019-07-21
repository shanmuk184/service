from tornado.gen import coroutine, Return
from api.stores.group import Group
from api.stores.user import GroupMapping, SupportedRoles, User, StatusType
from db import QueryConstants

class GroupModel(object):
    def __init__(self, user, db):
        self._user = user
        self.db = db



