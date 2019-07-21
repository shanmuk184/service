from motor.motor_tornado import MotorClient
import os
import configparser
from .db import Database
from tornado.gen import coroutine, Return

class DataBaseConnectionTestCase:
    def __init__(self):
        database = Database()
        self.db = database.db

    @coroutine
    def create_test_user(self):
        yield self.db.user.insert_one({})

