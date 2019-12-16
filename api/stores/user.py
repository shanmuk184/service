from enum import Enum
from .base import BaseStoreModel
import re
from bson import ObjectId
import uuid
import datetime
from tornado_swirl.swagger import schema
class SupportedRoles:
    Admin = 'ad'
    Member = 'me'

class DisplayRoles:
    Employee = 'Employee'
    Owner = 'Owner'

class UserStatus:
    Invited = 'invited'
    Registered = 'registered'

class EmailValidationStatus:
    Validated = 'validated'
    NotValidated = 'not_validated'

class NewUserStatus:
    Yes = 'yes'
    No = 'no'

@schema
class RegisterRequestParams:
    """
    Properties:
        name (str) -- Required Shanmuk
        email (email) -- Required
        phone (str) -- Required
        employeeid (int) -- Required
        password (password) -- Required
    """
    Name = 'name'
    Email = 'email'
    Phone = 'phone'
    EmployeeId = 'employeeid'
    Password = 'password'

@schema
class LoginRequestParams:
    """
    Properties:
        username (email) -- Required
        password (password) -- Required
    """
    UserName = 'username'
    Password = 'password'

@schema
class SuccessResponse:
    """
    Properties:
        status (str) -- Required
        authToken (str) -- Required
    """
    Status = 'status'
    AuthToken = 'authToken'


class LinkedAccountType:
    Native = 'native'

class StatusType:
    Invited = 'invited'
    Accepted = 'accepted'

class GroupMapping(BaseStoreModel):
    class PropertyNames:
        GroupId ='group_id'
        Roles = 'roles'
        Status = 'status'
        Shifts = 'shift'
        Tasks = 'tasks'


    @property
    def GroupId(self):
        return self.get_value(self.PropertyNames.GroupId)

    @GroupId.setter
    def GroupId(self, group_id):
        return self.set_value(self.PropertyNames.GroupId, group_id)


    @property
    def Roles(self):
        return self.get_value(self.PropertyNames.Roles)

    @property
    def Status(self):
        return self.get_value(self.PropertyNames.Status)

    @Status.setter
    def Status(self, status):
        if not status:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Status, status)



    @Roles.setter
    def Roles(self, roles):
        if not isinstance(roles, list):
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Roles, roles)

class LinkedAccount(BaseStoreModel):
    def __init__(self,accountname=None, accounthash=None, accounttype=None, **kwargs):
        super().__init__()
        if accountname and accounthash:
            self.set_value(self.PropertyNames.AccountName, accountname)
            self.set_value(self.PropertyNames.AccountHash, accounthash)

    @property
    def AccountName(self):
        return self.get_value(self.PropertyNames.AccountName)

    @AccountName.setter
    def AccountName(self, accountname):
        if not accountname:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.AccountName, accountname)

    @property
    def AccountHash(self):
        return self.get_value(self.PropertyNames.AccountHash)


    @AccountHash.setter
    def AccountHash(self, accounthash):
        if not accounthash:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.AccountHash, accounthash)

    @property
    def AccountType(self):
        return self.get_value(self.PropertyNames.AccountType)

    @AccountType.setter
    def AccountType(self, accounttype):
        if not accounttype:
            raise NotImplemented()

    class PropertyNames:
        AccountName = 'accountname'
        AccountHash = 'accounthash'
        AccountType = 'accounttype'
        AuthToken = 'authtoken'
    _reverseMapping = {
        'accountname':('AccountName', str),
        'accounthash':('AccountHash', str),
        'accounttype': ('AccountType', str),
        'authtoken': ('AuthToken', str),
    }

    @property
    def AuthToken(self):
        return self.get_value(self.PropertyNames.AuthToken)

    @AuthToken.setter
    def AuthToken(self, auth_token):
        return self.set_value(self.PropertyNames.AuthToken, auth_token)

    class ReverseMapping:
        accountname = 'AccountName'
        accounthash = 'AccountHash'


@schema
class ProfileSchema:
    """
    Properties:
        _id (str) -- Userid
        primaryemail (email) -- Email
        phone (str) -- Phone
        employeeid -- EmployeeId
    """
    pass


class User(BaseStoreModel):
    '''
    This Design assumes All other baseModels are populated and entered into user

    '''

    @property
    def UserId(self):
        return self.get_value(self.PropertyNames.UserId)

    @UserId.setter
    def UserId(self, userId):
        if not userId:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.UserId, userId)

    @property
    def PrimaryEmail(self):
        return self.get_value(self.PropertyNames.PrimaryEmail)


    @PrimaryEmail.setter
    def PrimaryEmail(self, primaryemail):
        if not primaryemail:
            raise NotImplementedError()
        isValid = re.search('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',primaryemail)
        if isValid:
            self.set_value(self.PropertyNames.PrimaryEmail, primaryemail)
        else:
            raise ValueError('you must enter valid email')

    @property
    def LinkedAccounts(self):
        return self.get_value(self.PropertyNames.LinkedAccounts)


    @LinkedAccounts.setter
    def LinkedAccounts(self, linkedAccounts:list):
        '''Accepts array argument to be set'''
        if not linkedAccounts:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.LinkedAccounts, linkedAccounts)

    @property
    def Groups(self):
        return self.get_value(self.PropertyNames.Groups)

    @Groups.setter
    def Groups(self, groups:list):
        if not groups:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Groups, groups)

    @property
    def Name(self):
        return self.get_value(self.PropertyNames.Name)

    @Name.setter
    def Name(self, name:str):
        if not name:
            raise NotImplementedError('you must enter name')
        self.set_value(self.PropertyNames.Name, name)
    @property
    def EmployeeId(self):
        return self.get_value(self.PropertyNames.EmployeeId)

    @EmployeeId.setter
    def EmployeeId(self, employeeId:int):
        if not employeeId:
            raise NotImplementedError('you must enter employee id')
        self.set_value(self.PropertyNames.EmployeeId, employeeId)

    @property
    def Phone(self):
        return self.get_value(self.PropertyNames.Phone)

    @Phone.setter
    def Phone(self, phone: str):
        if not phone:
            raise NotImplementedError('you must enter phone')
        self.set_value(self.PropertyNames.Phone, phone)

    _reverseMapping = {
        '_id': ('UserId', ObjectId),
        'name':('Name', str),
        'primaryemail': ('PrimaryEmail', str),
        'linkedaccounts': ('LinkedAccounts', list, LinkedAccount),
        'groups': ('Groups', list, GroupMapping),
        'phone': ('Phone', str),
        'employeeid':('EmployeeId', int),
        'status':('Status',str),
        'emailvalidated':('EmailValidated', bool),
        'cts':('CreatedTimeStamp', datetime.datetime),
        'uts': ('UpdatedTimeStamp', datetime.datetime)
    }

    class PropertyNames:
        UserId = '_id'
        Name = 'name'
        PrimaryEmail = 'primaryemail'
        LinkedAccounts = 'linkedaccounts'
        Groups = 'groups'
        Phone = 'phone'
        EmployeeId = 'employeeid'
        Status='status'
        EmailValidated='emailvalidated'
        CreatedTimeStamp = 'cts'
        UpdatedTimeStamp = 'uts'



    @property
    def Status(self):
        return self.get_value(self.PropertyNames.Status)

    @Status.setter
    def Status(self, status):
        if not status:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Status, status)



    @property
    def EmailValidated(self):
        return self.get_value(self.PropertyNames.EmailValidated)

    @EmailValidated.setter
    def EmailValidated(self, emv):
        if not emv:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.EmailValidated, emv)

    @property
    def CreatedTimeStamp(self):
        return self.get_value(self.PropertyNames.CreatedTimeStamp)

    @CreatedTimeStamp.setter
    def CreatedTimeStamp(self, jts):
        if not jts:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.CreatedTimeStamp, jts)


    @property
    def UpdatedTimeStamp(self):
        return self.get_value(self.PropertyNames.UpdatedTimeStamp)

    @UpdatedTimeStamp.setter
    def UpdatedTimeStamp(self, lts):
        if not lts:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.UpdatedTimeStamp, lts)


    #
    # def populate_data_dict(self,dictParam=None):
    #     self._data_dict = dictParam
    #     linkedAccountsList = dictParam.get(self.PropertyNames.LinkedAccounts)
    #     groupsList = dictParam.get(self.PropertyNames.Groups)
    #     linkedaccounts = []
    #     groups = []
    #     for linkedAccount in linkedAccountsList:
    #         linkedaccount = LinkedAccount()
    #         linkedaccount.populate_data_dict(linkedAccount)
    #         linkedaccounts.append(linkedAccount)
    #     if groupsList:
    #         for group in groupsList:
    #             groupMapping = GroupMapping()
    #             groupMapping.populate_data_dict(group)
    #             groups.append(groupMapping)
    #     self.set_value(self.PropertyNames.LinkedAccounts, linkedaccounts)
    #     if groupsList:
    #         self.set_value(self.PropertyNames.Groups, groups)

#
# class UserRegistrationForm(BaseApiModel):
#     _fields = ()

