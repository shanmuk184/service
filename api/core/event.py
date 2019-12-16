from tornado.gen import *
from db.db import Database

class EventHelper:
    def __init__(self, user, db):
        if user:
            self._user = user
        if not db:
            raise ValueError('db should be present')
        database = Database(db)
        self.db = database

    @coroutine
    def create_event(self, eventDict):
        try:
            event_result = yield self.db.EventCollection.insert_one(eventDict)
        except:
            pass
        else:
            raise Return((event_result))

