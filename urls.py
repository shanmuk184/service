from api.handlers.user import RegisterHandler, LoginHandler

urlpatterns = [
    (r"/api/register$", RegisterHandler),
    (r"/api/login$",LoginHandler )
]
