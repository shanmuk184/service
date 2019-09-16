from api.stores.base import BaseStoreModel
from bson import ObjectId
class Product(BaseStoreModel):
    class PropertyNames:
        Name = 'name'
        ProductCode = 'pc'
        ProductId = 'pId'
        GroupId = 'groupid'


    # _reverseMapping={
    #     '_id':(_id, ObjectId),
    #     'pc':(ProductCode, str),
    #     'name':('Name', str),
    #     'pId':('ProductId', str)
    # }

    @property
    def Name(self):
        name = self.get_value(self.PropertyNames.Name)
        if name:
            return name
    @Name.setter
    def Name(self, name):
        if not name:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.Name, name)

    @property
    def GroupId(self):
        name = self.get_value(self.PropertyNames.GroupId)

        return name
    @GroupId.setter
    def GroupId(self, groupId):
        if not groupId:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.GroupId, groupId)

    @property
    def ProductCode(self):
        productcode = self.get_value(self.PropertyNames.ProductCode)

        return productcode
    @ProductCode.setter
    def ProductCode(self, productcode):
        if not productcode:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.ProductCode, productcode)


    @property
    def ProductId(self):
        productid = self.get_value(self.PropertyNames.ProductId)
        return productid

    @ProductId.setter
    def ProductId(self, productid):
        if not productid:
            raise NotImplementedError()
        self.set_value(self.PropertyNames.ProductId, productid)
