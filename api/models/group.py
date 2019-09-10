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
        if self.db:
            self._gh = GroupHelper(self._user, self.db)
            self._uh = UserHelper(self._user, self.db)

    @coroutine
    def create_group(self, groupDict):
        group = Group()
        group.Name = groupDict.get(Group.PropertyNames.Name)
        group.OwnerId = self._user.UserId
        group_result = yield self._gh.create_group_for_user(group.datadict)
        if group_result:
            groupMemberMapping = self._gh.create_member_mapping(self._user.UserId, [SupportedRoles.Admin])
            yield self._gh.insert_member_mapping_into_group(group_result.inserted_id, groupMemberMapping.datadict)
            memberGroupMapping = self._uh.create_group_mapping(group_result.inserted_id, [SupportedRoles.Admin])
            yield self._gh.insert_group_mapping_into_user(self._user.UserId, memberGroupMapping.datadict)
        raise Return(group)
