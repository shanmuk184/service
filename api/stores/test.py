from user import User

if __name__ == "__main__":

    user = User()
    user.primary_email = 'me'
    user.companyname = 'me'
    user.LinkedAccounts.accountname = 'me'
    user.LinkedAccounts.accounthash = 'me'

    user.populate_data_dict()
    print(user.data_dict)
