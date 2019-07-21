from motor.motor_tornado import MotorClient, MotorCollection
from config import Settings
from enum import Enum
from tornado.gen import coroutine, Return
settings = Settings()

class QueryConstants(Enum):
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
    def UserCollection(self):
        if not self.db:
           raise NotImplementedError()


        raise Return(self.db.get_collection(self.CollectionNames.User))



    @property
    def GroupCollection(self):
        if not self.db:
           raise NotImplementedError()
        raise Return(self.db.get_collection(self.CollectionNames.Group))

    def get_database(self):
        port = int(settings.DbPort)
        conn = MotorClient(settings.DbHost, port)
        return conn.get_database(settings.DbName)