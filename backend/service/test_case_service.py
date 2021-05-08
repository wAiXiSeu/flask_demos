# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2021/4/29'
__description__ = doc description
"""
from collections import defaultdict
from datetime import datetime

from core.cache import cache
from core.db.mongo_helper import MongoHelper
from core.db.mysql_helper import mysql

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
    r = t.get("results") if t else []
    d = get_doctor_result(case_id, '')
    table = {_.get("qc_id"): (_.get("doctor_result"), _.get("errorReason")) for _ in d}
    for _ in r:
        k = _fmt_check_id(_['check_id'])
        if k in table:
            _['doctor_result'] = table[k][0]
            _['error_reason'] = table[k][1]
        else:
            _['doctor_result'] = '无'
            _['error_reason'] = ''
    return r


def _fmt_check_id(check_id):
    """
    将S0058_1 -> S0058
    :param check_id:
    :return:
    """
    if not check_id:
        return ''
    k = check_id.split('_')[0].upper()
    if k.startswith("YF"):
        k = str(int(k[2:]))
    return k


def delete_test_data():
    """
    删除数据库test_data，软删除，重命名
    :return:
    """
    cache.delete_memoized(get_doctor_result)
    suffix = datetime.now().strftime("%Y%m%d%H%M")
    return qc_collection.rename(f"test_data_{suffix}")


@cache.memoize(timeout=24*60*60)
def get_doctor_result(case_id, qc_id: str):
    sql = "select * from DoctorResult where 1=1"
    if case_id:
        sql += f" and caseId='{case_id}'"
    if qc_id:
        sql += f" and qc_id='{qc_id.upper()}'"
    sql += ";"
    r = mysql.query(sql=sql)
    case_ids = list(set([_.get("caseId") for _ in r]))
    t = qc_collection.find({"rid": {"$in": case_ids}})
    table = defaultdict(dict)
    for _ in t:
        results = _.get("results")
        for _r in results:
            k = _fmt_check_id(_r.get("check_id"))
            table[_.get("rid")][k] = str(_r.get("code"))
    for _ in r:
        ci = _['caseId']
        _["code"] = table[ci].get(_["qc_id"], '') if ci in table else ''
    return r
