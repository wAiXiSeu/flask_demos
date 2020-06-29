# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020-06-12'
__description__ = doc description
"""
from core.db.mongo_helper import MongoHelper

case_info_collection = MongoHelper(database="ai-test-cases").get_collection("case_info")


def list_cases():
    pass


def upsert_cases(body):
    pass


def delete_cases(body):
    pass


