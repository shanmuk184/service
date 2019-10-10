from api.handlers.user import *
from api.handlers.group import CreateGroupHandler, GroupsListHandler
from api.handlers.product import ProductHandler
from api.handlers.event import EventHandler


urlpatterns = [
    (r"/api/register$", RegisterHandler),
    (r"/api/login$",LoginHandler ),
    (r'/api/profile', ProfileHandler),
    (r'/api/employee$', ),
    (r'/api/group$', CreateGroupHandler),
    (r'/api/product', ProductHandler),
    (r'/api/event', EventHandler),
    (r'/api/groups', GroupsListHandler)
]
