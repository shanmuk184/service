from motor.motor_tornado import MotorClient, MotorCollection
from config import Settings
from enum import Enum
from tornado.gen import coroutine, Return

settings = Settings()
class QueryConstants:
    Set = '$set'
    AddToSet = '$addToSet'

class Database:
    def __init__(self, db=None):
        self.db = self.get_motor_connection()

    class CollectionNames:
        User = 'user'
        Group = 'group'
        Attendance = 'attendance'
        Event = 'event'
        Product = 'product'

    @property
    def UserCollection(self, *args, **kwargs):
        if not self.db:
           raise NotImplementedError()
        user = self.db[self.CollectionNames.User]
        return user

    @property
    def GroupCollection(self):
        if not self.db:
           raise NotImplementedError()
        return self.db[self.CollectionNames.Group]
    @property
    def ProductCollection(self):
        if not self.db:
            raise NotImplementedError()
        return self.db[self.CollectionNames.Product]

    @property
    def EventCollection(self):
        if not self.db:
            raise NotImplementedError()
        return self.db[self.CollectionNames.Event]

    def get_motor_connection(self):
        port = int(settings.DbPort)
        conn = MotorClient(settings.DbHost, port)
        db = getattr(conn, 'dev')
        return db