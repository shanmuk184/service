from api.stores.user import User
def test_user():
    user = User()
    user.PrimaryEmail = 'abc'
    print(user.datadict)
