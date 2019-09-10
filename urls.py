from api.handlers.user import *

urlpatterns = [
    (r"/api/register$", RegisterHandler),
    (r"/api/login$",LoginHandler ),
    (r'/api/profile', ProfileHandler)

]
