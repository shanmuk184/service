from enum import Enum
from .base import BaseStoreModel

class SupportedRoles:
    Admin = 'ad'
    Member = 'me'

class DisplayRoles(Enum):
    Employee = 'Employee'
    Owner = 'Owner'


class StatusType(Enum):
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
        return self._data_dict.get(self.PropertyNames.AccountHash)


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

    @property
    def AuthToken(self):
        return self.get_value(self.PropertyNames.AuthToken)

    @AuthToken.setter
    def AuthToken(self, auth_token):
        return self.set_value(self.PropertyNames.AuthToken, auth_token)

    class ReverseMapping:
        accountname = 'AccountName'
        accounthash = 'AccountHash'

    def populate_data_dict(self, dict=None):
        if dict:
            self.populate_data_dict(dict)



class User(BaseStoreModel):
    '''
    This Design assumes All other baseModels are populated and entered into user
    '''
    def __init__(self, **kwargs):
        super().__init__()

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
        print(self.PropertyNames.PrimaryEmail)
        self.set_value(self.PropertyNames.PrimaryEmail, primaryemail)


    @property
    def LinkedAccounts(self):
        return self.get_value(self.PropertyNames.LinkedAccounts)


    @LinkedAccounts.setter
    def LinkedAccounts(self, linkedAccounts:list):
        '''Accepts array argument to be set'''
        if not linkedAccounts:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.PrimaryEmail, linkedAccounts)

    @property
    def LinkedAccounts(self):
        return self.get_value(self.PropertyNames.LinkedAccounts)


    @LinkedAccounts.setter
    def LinkedAccounts(self, linkedAccounts:list):
        '''Accepts array argument to be set'''
        if not linkedAccounts:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.PrimaryEmail, linkedAccounts)




    @property
    def Groups(self):
        return self.get_value(self.PropertyNames.Groups)

    @Groups.setter
    def Groups(self, groups:list):
        if not groups:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Groups, groups)

    DbPropertiesDict = {
        '_id': 'UserId',
        'primaryemail': 'PrimaryEmail',
        'linkedaccounts': 'LinkedAccounts',
        'groups': 'Groups'
    }

    class PropertyNames:
        UserId = '_id'
        PrimaryEmail = 'primary_email'
        CompanyName = 'companyname'
        LinkedAccounts = 'linkedaccounts'
        Groups = 'groups'

    def populate_data_dict(self,dictParam=None):
        self._data_dict = dictParam
        linkedAccountsList = dictParam.get(self.PropertyNames.LinkedAccounts)
        linkedaccounts = []
        for linkedAccount in linkedAccountsList:
            linkedaccount = LinkedAccount()
            linkedaccount.populate_data_dict(linkedAccount)
            linkedaccounts.append(linkedAccount)
        self.set_value(self.PropertyNames.LinkedAccounts, linkedaccounts)
