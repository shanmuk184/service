from tornado.gen import coroutine, Return
from api.stores.group import Group, GroupType
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
    def __init__(self, **kwargs):
        if not kwargs.get('db'):
            raise ValueError('db should be present')
        if kwargs.get('user'):
            self._user = kwargs.get('user')
        self.db = kwargs.get('db')

        if self._user:
            self._gh = GroupHelper(**kwargs)
            self._uh = UserHelper(**kwargs)
        elif self.db:
            self._gh = GroupHelper(db=self.db)
            self._uh = UserHelper(db=self.db)

    @coroutine
    def create_group(self, groupDict, userId, type):
        group = Group()
        group.Name = groupDict.get(Group.PropertyNames.Name)
        group.OwnerId = userId
        group.Type = type
        group.MemberMappings.append(self._gh.create_member_mapping(self._user.UserId, [SupportedRoles.Admin]))
        group.set_value(group.PropertyNames.CreatedTimeStamp, datetime.datetime.now())
        group.set_value(group.PropertyNames.UpdatedTimeStamp, datetime.datetime.now())
        group_result = yield self._gh.create_group_for_user(group.datadict)
        group.Id = group_result.inserted_id
        memberGroupMapping = self._uh.create_group_mapping(group_result.inserted_id, [SupportedRoles.Admin])
        yield self._gh.insert_group_mapping_into_user(self._user.UserId, memberGroupMapping.datadict)
        raise Return(group)

    # Pharmaceutical distributor is a kind of group that don't have link to Pharmacy company only reverse link
    @coroutine
    def create_pharmaceutical_distributor(self, **kwargs):
        group = self.create_group(kwargs, self._user.UserId, GroupType.PharmaDistributor)
        raise Return(group)
    # Dummy team for employees
    @coroutine
    def create_employee_team(self, **kwargs):
        group = self.create_group(kwargs, self._user.UserId, GroupType.EmployeeTeam)
        raise Return(group)

    @coroutine
    def create_pharmaceutical_distributor(self, **kwargs):
        group = self.create_group(kwargs, GroupType.PharmaCompany)

    @coroutine
    def get_groups_for_user(self, userId):
        if not userId:
            userId = self._user.UserId
        try:
            (groups) = yield self._gh.get_groups_for_user(userId)
        except Exception as e:
            raise Return((False, str(e)))
        else:
            raise Return((True, groups))