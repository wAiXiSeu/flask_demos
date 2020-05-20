# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-12-30'
__description__ = doc description
"""
import os

from pymongo import MongoClient


class MongoHelper(object):
    def __init__(self, host, port, user, password, database):
        self.host = os.getenv("MONGO_HOST", host)
        self.port = os.getenv("MONGO_PORT", port)
        self.username = os.getenv("MONGO_USERNAME", user)
        self.password = os.getenv("MONGO_PASSWORD", password)
        self.database = os.getenv("MONGO_DATABASE", database)
        self.uri = "mongodb://{host}:{port}".format(host=self.host, port=self.port)
        self.client = MongoClient(self.uri)

    def get_client(self):
        return self.client

    def get_database(self):
        if self.username and self.password:
            self.client[self.database].authenticate(self.username, self.password)
        return self.client[self.database]

    def get_collection(self, collection_name):
        db = self.get_database()
        return db[collection_name]
