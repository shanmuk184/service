from .base import BaseStoreModel
from enum import Enum

class GroupType(Enum):
    Restaurent = 'res'



class Group(BaseStoreModel):
    class PropertyNames:
        UserId = '_id'
        Name = 'name'
        EmployeeCount = 'employee_count'
        Admins = 'admins'
        Type = 'type'

    @property
    def Name(self):
        return self.get_value(self.PropertyNames.Name)
    @Name.setter
    def Name(self, name):
        if not name:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Name, name)

    @property
    def Admins(self):
        self.get_value(self.PropertyNames.Admins)

    @Admins.setter
    def Admins(self, adminids):
        if not isinstance(adminids, list):
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Admins, adminids)

    @property
    def Type(self):
        return self.get_value(self.PropertyNames.Type)

    @Type.setter
    def Type(self, type):
        if not type:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Type, type)

