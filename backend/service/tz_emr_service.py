# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020-06-29'
__description__ = doc description
"""
import functools
import os

from pymongo import MongoClient

collection = MongoClient(host=os.getenv("MONGO_HOST", "192.168.101.173"),
                         port=int(os.getenv("MONGO_PORT", "47017"))) \
    .get_database(os.getenv("MONGO_DB", "zjtz")).get_collection('emr')


def get_vid_list():
    return list(collection.distinct("vid"))


@functools.lru_cache()
def get_doc_list(vid):
    info = collection.find({'vid': vid}, {'_id': 0})
    return [t.get('doc') for t in info]


@functools.lru_cache()
def get_details(vid, doc):
    info = collection.find_one({'vid': vid, 'doc': doc}, {'_id': 0})
    return info.get('html')
