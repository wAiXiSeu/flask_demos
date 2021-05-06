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

from core.loggers import LocalLogger


class MongoHelper:
    def __init__(self, host="localhost", port=27017, database="", **kwargs):
        self.host = os.getenv("MONGO_HOST", host)
        self.port = os.getenv("MONGO_PORT", port)
        self.username = os.getenv("MONGO_USERNAME", kwargs.get("user"))
        self.password = os.getenv("MONGO_PASSWORD", kwargs.get("password"))
        self.database = os.getenv("MONGO_DATABASE", database)
        self.uri = "mongodb://{host}:{port}".format(host=self.host, port=self.port)
        self.client = MongoClient(self.uri)

    def get_client(self):
        return self.client

    def get_database(self):
        LocalLogger.info(
            "try to connect to {}, database: {}".format(
                "mongodb://{host}:{port}".format(host=self.host, port=self.port), self.database),
            msg_type="MongoDB", where="MongoHelper.get_database")
        if self.username and self.password:
            self.client[self.database].authenticate(self.username, self.password)
        return self.client[self.database]

    def get_collection(self, collection_name):
        db = self.get_database()
        return db[collection_name]
