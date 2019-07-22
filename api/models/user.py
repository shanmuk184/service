from tornado.gen import *
import bcrypt
import jwt
import base64
from api.stores.user import User, LinkedAccount
from api.core.user import UserHelper
from api.core.group import GroupHelper
import tornado.ioloop


class UserModel(object):
    def __init__(self, user, db):
        self._user = user
        self.db = db
        self._uh = UserHelper(self._user, self.db)
        self._gh = GroupHelper(self._user, self.db)

    @coroutine
    def create_user(self, postBodyDict):
        """
        :param postBodyDict:
        username
        password
        password1
        email
        :return:
        """
        isValid = self.validate_password(postBodyDict)
        if not postBodyDict.get('email'):
            raise Return({'status':'error', 'message':'you must enter email'})

        if isValid and isValid.get('status') == 'error':
            raise Return(isValid)

        user = User()
        user.PrimaryEmail = postBodyDict['email']
        password = yield self.get_hashed_password(postBodyDict['password'])
        linkedaccount = LinkedAccount()
        linkedaccount.AccountName = postBodyDict['email']
        linkedaccount.AccountHash = password['hash']
        user.LinkedAccounts = [linkedaccount]
        user_result = yield self._uh.save_user(user.datadict)

        if not user_result.acknowledged:
            raise NotImplementedError('Db error thrown')

        group = yield self._gh.createDummyGroupForUser(user_result.inserted_id)
        if not group.acknowledged:
            raise NotImplementedError('Db error')
        yield self._gh.createGroupMemberMappingForDummyGroup(group.inserted_id, user_result.inserted_id)
        raise Return({'status':'success'})



    def validate_password(self, postBodyDict):
        if postBodyDict['password'] != postBodyDict['password2']:
            return {'status':'error', 'message':'you must enter same password'}

    @coroutine
    def get_hashed_password(self, plain_text_password):
        raise Return({'hash':bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt(12))})


    @coroutine
    def check_hashed_password(self, text_password, hashed_password):
        raise Return(bcrypt.checkpw(text_password.encode('utf-8'), hashed_password))

    @coroutine
    def login(self, dict):
        username = dict.get('username')
        password = dict.get('password')
        try:
            user = yield self._uh.getUserByUsername(username)
            linkedAccount = user.LinkedAccounts[0]
            accounthash = linkedAccount.get(LinkedAccount.PropertyNames.AccountHash)
            isvalidPassword = yield self.check_hashed_password(password, accounthash)
            if isvalidPassword:
                raise Return((True, user))
            else:
                raise Return((False,'Wrong password'))
        except IndexError:
            raise Return((False, 'user email does not exist'))