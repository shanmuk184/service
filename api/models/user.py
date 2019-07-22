from tornado.gen import *
import bcrypt
import jwt
import base64
from api.stores.user import User, LinkedAccount, LinkedAccountType
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
        try:
            user = User()
            user.PrimaryEmail = postBodyDict.get('email')
            password = yield self.get_hashed_password(postBodyDict.get('password'))
            linkedaccount = LinkedAccount()
            linkedaccount.AccountName = postBodyDict.get('email')
            linkedaccount.AccountHash = password.get('hash')
            linkedaccount.AccountType = LinkedAccountType.Native
            user.LinkedAccounts = [linkedaccount]
            user_result = yield self._uh.save_user(user.datadict)
            group = yield self._gh.createDummyGroupForUser(user_result.inserted_id)
            yield self._gh.createGroupMemberMappingForDummyGroup(group.inserted_id, user_result.inserted_id)
            raise Return((True, user_result.inserted_id))
        except Exception as e:
            raise Return((False, str(e)))


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
        if not username or not password:
            raise Return((False, 'You must enter both fields'))

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
        except Exception as e:
            raise Return((False, 'error'))