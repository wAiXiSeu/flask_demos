# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2021/4/29'
__description__ = doc description
"""
import os
from collections import defaultdict
from datetime import datetime
from urllib.parse import quote

from flask import make_response

from core.cache import cache
from core.db.mongo_helper import MongoHelper
from core.db.mysql_helper import mysql

from io import BytesIO

import pandas as pds

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
    t = qc_collection.find_one({'request.caseId': case_id}, {'results': 1})
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
    cache.delete_memoized_verhash(get_doctor_result)
    suffix = datetime.now().strftime("%Y%m%d%H%M")
    return qc_collection.rename(f"test_data_{suffix}")


def remove_cache():
    cache.clear()


def download_test_data():
    """
    下载所有数据
    :return:
    """
    out = BytesIO()
    writer = pds.ExcelWriter(out, engine='xlsxwriter')
    workbook = writer.book
    table = workbook.add_worksheet()
    dump_data = qc_collection.find()
    # write header
    columns = [
        "caseId",
        "check_id",
        "code",
        "doc_id",
        "message",
    ]
    for i, c in enumerate(columns):
        table.write(0, i, c)
    # write data
    count = 1
    for c in dump_data:
        req = c.get("request")
        r = c.get("results")
        for _r in r:
            table.write(count, 0, req.get("caseId"))
            table.write(count, 1, str(_r.get("check_id", "")))
            table.write(count, 2, str(_r.get("code", "")))
            table.write(count, 3, ','.join(_r.get("doc_id", [])))
            table.write(count, 4, _r.get("message", ""))
            count += 1
    workbook.close()
    out.seek(0)
    resp = make_response(out.getvalue())
    resp.headers["Content-Disposition"] = "attachment; filename=cases.xlsx"
    resp.headers['Content-Type'] = 'application/x-xlsx'
    return resp


@cache.memoize(timeout=24*60*60)
def get_doctor_result(case_id, qc_id: str):
    sql = "select * from doctorResult_all where hospital='溧水'"
    if case_id:
        sql += f" and case_id='{case_id}'"
    if qc_id:
        sql += f" and qc_id='{qc_id.upper()}'"
    sql += ";"
    r = mysql.query(sql=sql)
    case_ids = list(set([_.get("case_id") for _ in r]))
    t = qc_collection.find({"request.caseId": {"$in": case_ids}})
    table = defaultdict(dict)
    for _ in t:
        results = _.get("results")
        req = _.get("request")
        for _r in results:
            k = _fmt_check_id(_r.get("check_id"))
            table[req.get("caseId")][k] = str(_r.get("code"))
    for _ in r:
        ci = _['case_id']
        _["code"] = table[ci].get(_["qc_id"], '') if ci in table else ''
    return r
