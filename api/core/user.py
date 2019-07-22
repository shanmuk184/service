from tornado.gen import *
from api.stores.user import User, LinkedAccount
from db import Database
from tornado.ioloop import IOLoop
class UserHelper:
    def __init__(self, user, db):
        self._user = user
        database = Database(db)
        self.db = database

    @coroutine
    def save_user(self, user:dict):
        user = yield self.db.UserCollection.insert_one(user)
        raise Return(user)

    @coroutine
    def getUserByUsername(self, username):
        user = yield self.db.UserCollection.find_one({User.PropertyNames.PrimaryEmail: username})
        if user:
            userprofile = User()
            userprofile.populate_data_dict(user)
            raise Return(userprofile)
        else:
            raise IndexError('No User found')

    @coroutine
    def updateUserAuthToken(self, userId:bytes, authToken:bytes):
        criteria = {}
        criteria[User.PropertyNames.UserId] =  userId
        updateDict = {}

        updateDict[User.PropertyNames.LinkedAccounts+'.'+LinkedAccount.PropertyNames.AuthToken] = authToken
        yield self.db.UserCollection.update(criteria, updateDict)

