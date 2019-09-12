from tornado.gen import *
from .baseHandler import BaseHandler
from api.models.group import GroupModel
from api.models.Product import ProductModel
import json
from tornado import web

class ProductHandler(BaseHandler):
    @coroutine
    def post(self):
        user = yield self.current_user
        model = ProductModel(user, self.db)
        try:
            yield model.create_product_for_group(self.args)
        except Exception as e:
            print(str(e))
        self.finish(json.dumps({'status':'success'}))