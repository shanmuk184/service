from tornado.gen import coroutine, Return
from api.stores.group import Group
from api.stores.user import GroupMapping, SupportedRoles, User, StatusType
from db import QueryConstants
from tornado.gen import *
import bcrypt
import jwt
import base64
from api.stores.user import User, LinkedAccount, LinkedAccountType
from api.core.user import UserHelper
from api.core.group import GroupHelper
from api.core.product import ProductHelper
from api.stores.product import Product


class ProductModel(object):
    def __init__(self, user=None, db=None):
        if not db:
            raise ValueError('db should be present')
        if user:
            self._user = user
        self.db = db
        if self.db:
            self._gh = GroupHelper(self._user, self.db)
            self._uh = UserHelper(self._user, self.db)
            self._ph= ProductHelper(self._user, self.db)

    @coroutine
    def create_product_for_group(self, productDict):
        if not productDict:
            raise Return((False))

        product = Product()
        product.Name = productDict.get(product.PropertyNames.Name)
        product.ProductCode = productDict.get(product.PropertyNames.ProductCode)
        product.ProductId = productDict.get(product.PropertyNames.ProductId)
        product.GroupId = productDict.get(product.PropertyNames.GroupId)
        product_result = yield self._ph.create_product(product.datadict)

