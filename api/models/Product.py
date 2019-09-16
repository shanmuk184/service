from tornado.gen import *
from api.core.product import ProductHelper
from api.stores.product import Product
from api.models.base import BaseModel

class ProductModel(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._ph = ProductHelper(**kwargs)

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

