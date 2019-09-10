from tornado.gen import coroutine, Return
from api.stores.group import Group
from api.stores.user import GroupMapping, SupportedRoles, User, StatusType
from db import QueryConstants
from tornado.gen import *
import bcrypt
import jwt
import base64
from api.stores.user import User, LinkedAccount, LinkedAccountType
from api.core.user import UserHelper
from api.core.group import GroupHelper

import tornado.ioloop


class GroupModel(object):
    def __init__(self, user=None, db=None):
        if not db:
            raise ValueError('db should be present')
        if user:
            self._user = user
        self.db = db

    # def create_group(self, groupDict):



