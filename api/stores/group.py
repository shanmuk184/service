from .base import BaseStoreModel
from enum import Enum
from bson import ObjectId

class GroupType(Enum):
    Restaurent = 'res'


class MemberMapping(BaseStoreModel):
    class PropertyNames:
        MemberId = 'member_id'
        CreatedTimeStamp = 'created_time_stamp'
        Roles = 'roles'
        Status = 'status'
        Shifts = 'shift'
        Tasks = 'tasks'

    @property
    def MemberId(self):
        return self.get_value(self.PropertyNames.MemberId)

    @MemberId.setter
    def MemberId(self, memberId):
        if not memberId:
            raise NotImplementedError('you must enter memberId')
        return self.set_value(self.PropertyNames.MemberId, memberId)

    @property
    def Roles(self):
        return self.get_value(self.PropertyNames.Roles)

    @Roles.setter
    def Roles(self, roles):
        if not roles:
            raise NotImplementedError('you must give roles')
        return self.set_value(self.PropertyNames.Roles, roles)


    @property
    def Status(self):
        return self.get_value(self.PropertyNames.Status)

    @Status.setter
    def Status(self, status):
        if not status:
            raise NotImplementedError('you must give roles')
        return self.set_value(self.PropertyNames.Status, status)


class Group(BaseStoreModel):
    class PropertyNames:
        UserId = '_id'
        Name = 'name'
        EmployeeCount = 'employee_count'
        OwnerId = 'owner_id'
        Type = 'type'
        MemberMappings = 'membermappings'


    @property
    def Name(self):
        return self.get_value(self.PropertyNames.Name)

    @Name.setter
    def Name(self, name):
        if not name:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Name, name)

    @property
    def OwnerId(self):
        self.get_value(self.PropertyNames.OwnerId)

    @OwnerId.setter
    def OwnerId(self, ownerid):
        if not ownerid:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.OwnerId, ownerid)

    @property
    def Type(self):
        return self.get_value(self.PropertyNames.Type)

    @Type.setter
    def Type(self, type):
        if not type:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Type, type)
