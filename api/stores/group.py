from .base import BaseStoreModel
from enum import Enum
from api.stores.product import Product
from bson import ObjectId
from datetime import datetime

class GroupType(Enum):
    Restaurent = 'res'
    PharmaCompany = 'phc'
    PharmaDistributor = 'phd'
    EmployeeTeam = 'emt'


class MemberMapping(BaseStoreModel):
    class PropertyNames:
        MemberId = 'member_id'
        Title = "Title"
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
    def Title(self):
        return self.get_value(self.PropertyNames.Title)

    @Title.setter
    def Title(self, title):
        if not title:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Title, title)

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
    #
    # @property
    # def CreatedTimeStamp(self):
    #     if not

class SubGroupType:
    EmployeeGroup = 'emg'

class SubGroup(BaseStoreModel):
    class PropertyNames:
        Name = 'name'
        Type = 'type'


    @property
    def Name(self):
        return self.get_value(self.PropertyNames.Name)

    @Name.setter
    def Name(self, name):
        if not name:
            raise NotImplementedError('you must give roles')
        return self.set_value(self.PropertyNames.Name, name)


    @property
    def Type(self):
        return self.get_value(self.PropertyNames.Type)

    @Type.setter
    def Type(self, subgroupType):
        if not subgroupType:
            raise NotImplementedError('you must give roles')
        return self.set_value(self.PropertyNames.Type, subgroupType)

class ProductMapping(BaseStoreModel):
    pass

class Group(BaseStoreModel):

    class PropertyNames:
        Id = '_id'
        Name = 'name'
        EmployeeCount = 'employee_count'
        OwnerId = 'owner_id'
        Type = 'type'
        MemberMappings = 'membermappings'
        Products = 'products'
        CreatedTimeStamp = 'cts'
        UpdatedTimeStamp = 'uts'

    _reverseMapping = {
        '_id': ('Id', ObjectId),
        'name':('Name', str),
        'employee_count': ('EmployeeCount', int),
        'owner_id': ('OwnerId', ObjectId),
        'membermappings': ('MemberMappings', list, MemberMapping),
        'products': ('Products', list, Product),
        'cts':('CreatedTimeStamp', datetime),
        'uts': ('UpdatedTimeStamp', datetime)
    }

    @property
    def Id(self):
        return self.get_value(self.PropertyNames.Id)
    @Id.setter
    def Id(self, id):
        if not id:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Id, id)


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

    @property
    def Products(self):
        return self.get_value(self.PropertyNames.Products)

    @Products.setter
    def Products(self, products):
        if not products:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Products, products)

    @property
    def MemberMappings(self):
        return self.get_value(self.PropertyNames.MemberMappings)

    @MemberMappings.setter
    def MemberMappings(self, membermappings):
        if not membermappings:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.MemberMappings, membermappings)

    # def populate_data_dict(self,dictParam=None):
    #     self._data_dict = dictParam
    #     productsList = dictParam.get(self.PropertyNames.Products)
    #     products = []
    #     for product in productsList:
    #         product = Product()
    #         product.populate_data_dict(product)
    #         products.append(product)
    #     self.set_value(self.PropertyNames.Products, products)