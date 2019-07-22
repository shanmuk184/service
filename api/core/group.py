from tornado.gen import *
from api.stores.group import Group
from api.stores.user import GroupMapping, SupportedRoles, User, StatusType
from db import QueryConstants
from db import Database

class GroupHelper:
    def __init__(self, user, db):
        self._user = user
        database = Database(db)
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
    def createGroupMemberMappingForDummyGroup(self, dummyGroupId, userId):
        groupMapping = GroupMapping()
        groupMapping.GroupId = dummyGroupId
        groupMapping.Roles = [SupportedRoles.Member]
        groupMapping.Status = StatusType.Accepted

        yield self.db.UserCollection.update_one({
            User.PropertyNames.UserId: userId
        },
            {
                QueryConstants.AddToSet: {
                    User.PropertyNames.Groups: groupMapping.datadict
                }})

