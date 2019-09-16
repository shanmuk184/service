from tornado.gen import *
import bcrypt
import jwt
import base64
from api.stores.user import User, LinkedAccount, LinkedAccountType, RegisterRequestParams
from api.stores.group import Group
from api.models.base import BaseModel
import tornado.ioloop


class UserModel(BaseModel):
    @coroutine
    def check_if_user_exists_with_same_email(self, email):
        if not email:
            raise NotImplementedError()
        user = yield self._uh.getUserByEmail(email)
        if user:
            raise Return((True, user))
        raise Return((False, None))

    @coroutine
    def check_if_user_exists_with_same_employee_id(self, employee_id):
        if not employee_id:
            raise NotImplementedError()
        user = yield self._uh.getUserByEmployeeId(employee_id)
        if user:
            raise Return((True, user))
        raise Return((False, None))

    @coroutine
    def create_user(self, postBodyDict):
        """
        :param postBodyDict:
        password
        email
        :return:
        """
        user = User()
        user.Name = postBodyDict.get(user.PropertyNames.Name)
        user.Phone = postBodyDict.get(user.PropertyNames.Phone)
        user.PrimaryEmail = postBodyDict.get(RegisterRequestParams.Email)
        employee_exists = False
        if postBodyDict.get(user.PropertyNames.EmployeeId):
            user.EmployeeId = postBodyDict.get(user.PropertyNames.EmployeeId)
            (employee_exists, _) = yield self.check_if_user_exists_with_same_employee_id(user.EmployeeId)
        (user_exists, _) = yield self.check_if_user_exists_with_same_email(user.PrimaryEmail)
        if user_exists or employee_exists:
            raise Return((False, 'User already exists'))
        password = yield self.get_hashed_password(RegisterRequestParams.Password)
        linkedaccount = LinkedAccount()
        linkedaccount.AccountName = user.PrimaryEmail
        linkedaccount.AccountHash = password.get('hash')
        linkedaccount.AccountType = LinkedAccountType.Native
        user.LinkedAccounts = [linkedaccount]
        user_result = yield self._uh.save_user(user.datadict)
        user = yield self._uh.getUserByUserId(user_result.inserted_id)

        # group = yield self._gh.createDummyGroupForUser(user_result.inserted_id)
        # yield self._gh.createGroupMemberMappingForDummyGroup(group.inserted_id, user_result.inserted_id)
        raise Return((True, user))


    @coroutine
    def get_profile(self):
        if self._user:
            raise Return(self._user.datadict)


    def validate_password(self, postBodyDict):
        if postBodyDict['password'] != postBodyDict['password2']:
            return {'status':'error', 'message':'you must enter same password'}

    @coroutine
    def get_hashed_password(self, plain_text_password:str):
        if not plain_text_password:
            raise NotImplementedError()
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
            user = yield self._uh.getUserByEmail(username)
            if user:
                linkedAccount = user.LinkedAccounts[0]
                accounthash = linkedAccount.get(LinkedAccount.PropertyNames.AccountHash)
                isvalidPassword = yield self.check_hashed_password(password, accounthash)
                if isvalidPassword:
                    raise Return((True, user))
                else:
                    raise Return((False,'Wrong password'))
            else:
                raise Return((False, 'user email does not exist'))
        except IndexError:
            raise Return((False, 'user email does not exist'))
