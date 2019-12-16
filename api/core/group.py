from tornado.gen import *
from api.stores.group import Group, MemberMapping
from api.stores.user import SupportedRoles, StatusType
from db.db import QueryConstants
from db.db import Database

class GroupHelper:
    def __init__(self,**kwargs):
        self._user = kwargs.get('user')
        database = Database(kwargs.get('db'))
        self.db = database


    @coroutine
    def createDummyGroupForUser(self, userid):
        if not userid:
            raise NotImplementedError()
        group = Group()
        group.Name = 'Dummy Group'
        group.Admins = [userid]
        group_result = yield self.db.GroupCollection.insert_one(group.datadict)
        raise Return(group_result)

    @coroutine
    def create_group_for_user(self, groupDict:dict):
        if not groupDict:
            raise Return('error')
        group = yield self.db.GroupCollection.insert_one(groupDict)
        raise Return(group)

    @coroutine
    def get_groups_for_user(self, userId):
        groupCursor = self.db.GroupCollection.find({Group.PropertyNames.OwnerId:userId})
        groups = []
        while (yield groupCursor.fetch_next):
            groupDict = groupCursor.next_object()
            groups.append(groupDict)
        raise Return((groups))

    def create_member_mapping(self, memberId, roles):
        memberMapping = MemberMapping()
        memberMapping.MemberId = memberId
        memberMapping.Roles = roles
        if SupportedRoles.Admin in roles:
            memberMapping.Status = StatusType.Accepted
        else:
            memberMapping.Status = StatusType.Invited
        return memberMapping

    @coroutine
    def insert_member_mapping_into_group(self, groupId, mappingDict):
        if not mappingDict or not groupId:
            raise NotImplementedError()
        yield self.db.GroupCollection.update({'_id':groupId}, {QueryConstants.AddToSet:{Group.PropertyNames.MemberMappings:mappingDict}}, w=1)

    @coroutine
    def insert_group_mapping_into_user(self, userId, mappingDict):
        if not mappingDict or not userId:
            raise NotImplementedError()
        user_result = yield self.db.UserCollection.update({'_id': userId}, {
            QueryConstants.AddToSet: {Group.PropertyNames.MemberMappings: mappingDict}}, w=1)
        raise Return(user_result)
