from tornado.gen import *
from api.core.event import EventHelper
from api.models.base import BaseModel


class EventModel(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._eh = EventHelper(**kwargs)


    @coroutine
    def create_event(self, eventDict):
        if not eventDict:
            raise NotImplementedError()
        yield self._eh.create_event(eventDict)
