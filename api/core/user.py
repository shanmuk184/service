from tornado.gen import *
from api.stores.user import User, LinkedAccount, GroupMapping, SupportedRoles, StatusType
from db.db import Database
from bson import ObjectId
class UserHelper:
    def __init__(self, user=None, db=None):
        if user:
            self._user = user
        if not db:
            raise ValueError('db should be present')
        database = Database(db)
        self.db = database

    @coroutine
    def save_user(self, user:dict):
        user_result=None
        try:
            user_result = yield self.db.UserCollection.insert_one(user)
        except Exception as e:
            print(str(e))
        raise Return(user_result)


    @coroutine
    def getUserByUserId(self, userId):
        userDict = yield self.db.UserCollection.find_one({'_id':ObjectId(userId)})
        if userDict:
            user = User()
            user.populate_data_dict(userDict)
            raise Return(user)
    @coroutine
    def getUserByEmployeeId(self, employeeId):
        if not employeeId:
            raise NotImplementedError('employee ')
        user = yield self.db.UserCollection.find_one({User.PropertyNames.EmployeeId: employeeId})
        if user:
            userprofile = User()
            userprofile.populate_data_dict(user)
            raise Return(userprofile)
        raise Return(None)

    def create_group_mapping(self, groupId, role):
        memberMapping = GroupMapping()
        memberMapping.GroupId = groupId
        memberMapping.Roles = [role]
        if role == SupportedRoles.Admin:
            memberMapping.Status = StatusType.Accepted
        else:
            memberMapping.Status = StatusType.Invited
        return memberMapping

    @coroutine
    def getUserByEmail(self, username):
        user = yield self.db.UserCollection.find_one({User.PropertyNames.PrimaryEmail: username})
        if user:
            userprofile = User()
            userprofile.populate_data_dict(user)
            raise Return(userprofile)

    @coroutine
    def updateUserAuthToken(self, userId:bytes, authToken:bytes):
        criteria = {}
        criteria[User.PropertyNames.UserId] =  userId
        updateDict = {}
        updateDict[User.PropertyNames.LinkedAccounts+'.'+LinkedAccount.PropertyNames.AuthToken] = authToken
        yield self.db.UserCollection.update(criteria, updateDict)
