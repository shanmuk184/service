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
        if db:
            self.db = db
    class CollectionNames:
        User = 'user'
        Group = 'group'
        Attendance = 'attendance'
        Shifts = 'shifts'



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
        group = self.db[self.CollectionNames.Group]
        return group

    def get_database(self):
        port = int(settings.DbPort)
        conn = MotorClient(settings.DbHost, port)
        db = getattr(conn, 'dev')
        return db