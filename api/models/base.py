from api.core.user import UserHelper
from api.core.group import GroupHelper

class BaseModel(object):
    def __init__(self, **kwargs):
        if not kwargs.get('db'):
            raise ValueError('db should be present')
        self._user = None
        if kwargs.get('user'):
            self._user = kwargs.get('user')
        self.db = kwargs.get('db')

        if self._user:
            self._gh = GroupHelper(**kwargs)
            self._uh = UserHelper(**kwargs)
        elif self.db:
            self._gh = GroupHelper(db=self.db)
            self._uh = UserHelper(db=self.db)
