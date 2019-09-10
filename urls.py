from api.handlers.user import *
from api.handlers.group import GroupHandler

urlpatterns = [
    (r"/api/register$", RegisterHandler),
    (r"/api/login$",LoginHandler ),
    (r'/api/profile', ProfileHandler),
    (r'/api/groups$', GroupHandler)

]
