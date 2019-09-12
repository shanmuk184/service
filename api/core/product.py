from tornado.gen import *
from api.stores.group import Group, MemberMapping
from api.stores.user import GroupMapping, SupportedRoles, User, StatusType
from api.stores.product import Product
from db import QueryConstants
from db import Database

class ProductHelper:
    def __init__(self, user, db):
        if user:
            self._user = user
        if not db:
            raise ValueError('db should be present')
        database = Database(db)
        self.db = database

    @coroutine
    def create_product(self, productDict):
        if not productDict:
            raise NotImplementedError()
        user_result = yield self.db.ProductCollection.insert_one(productDict)
        raise Return((user_result))

