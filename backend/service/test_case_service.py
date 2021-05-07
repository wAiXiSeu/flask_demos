# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2021/4/29'
__description__ = doc description
"""
from datetime import datetime

from core.db.mongo_helper import MongoHelper

try:
    import ujson as json
except:
    import json

db = MongoHelper(database='quality_control_actor')
case_collection = db.get_collection("cases")
qc_collection = db.get_collection('test_data')


def list_all_cases(hospital):
    """
    列出所有caseId
    :param hospital:
    :return:
    """
    tmp = case_collection.find({"hospital": hospital}, {"caseId": 1})
    return [_.get('caseId') for _ in tmp] if tmp else []


def get_emr(case_id, hospital):
    """
    通过caseId获取emr
    :param hospital:
    :param case_id:
    :return:
    """
    body = {
        "caseId": case_id
    }
    if hospital:
        body['hospital'] = hospital
    return case_collection.find_one(body, {"_id": 0})


def get_qc_result(case_id):
    """
    通过caseId 获取
    :param case_id:
    :return:
    """
    t = qc_collection.find_one({'rid': case_id}, {'results': 1})
    return t.get("results") if t else None


def delete_test_data():
    """
    删除数据库，软删除，重命名
    :return:
    """
    suffix = datetime.now().strftime("%Y%m%d%H%M")
    return qc_collection.rename(f"test_data_{suffix}")
