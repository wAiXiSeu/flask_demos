# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020-05-20'
__description__ = doc description
"""
from core.cache import cache
from core.db.mongo_helper import MongoHelper

logs_collection = MongoHelper(host="192.168.80.20", port=30217, database="qc2", password=None, user=None).get_collection("logs")


@cache.memoize()
def get_logs(rid: str):
    query = {"rid": rid}
    if rid.startswith("^"):
        query["rid"] = {"$regex": rid}
    res = logs_collection.find(query, {"_id": 0}).sort("rid", -1).limit(1)
    return list(res)


