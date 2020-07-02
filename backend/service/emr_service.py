# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020-06-29'
__description__ = doc description
"""
import os

import pymysql
from bs4 import BeautifulSoup
from pymongo import MongoClient

from core.cache import cache

db = MongoClient(host=os.getenv("MONGO_HOST", "localhost"),
                 port=int(os.getenv("MONGO_PORT", "27017"))).get_database(os.getenv("MONGO_DB", "syf_example"))

mysql = pymysql.connect(host=os.getenv("MYSQL_HOST", "localhost"),
                        port=int(os.getenv("MYSQL_PORT", "3306")),
                        user=os.getenv("MYSQL_USER", "root"),
                        password=os.getenv("MYSQL_PASS", "123456"), db="syf", charset="utf8")


def get_emr_list(collection_name):
    collection = db.get_collection(collection_name)
    return list(collection.distinct("caseId"))


def get_basic_info(case_id, table_name="emr"):
    collection = db.get_collection(table_name)
    info = collection.find_one({"caseId": case_id}, {"emr": 0, "_id": 0})
    return dict(info)


@cache.memoize(timeout=7 * 24 * 60 * 60, make_name="_emr_html_")
def get_by_id(case_id, filters, table_name="emr"):
    collection = db.get_collection(table_name)
    query = {"caseId": case_id}
    query.update(filters)
    info = collection.find_one(query, {"emr": 1})
    emr = info.get("emr") or {}
    res = {"inp_record": [], "first_page": []}
    titles = {"大病史", "入院记录", "出院记录", "死亡记录", "手术记录"}
    for k, v in emr.items():
        if "病案首页" in k:
            for c in v:
                res["first_page"].append({
                    "title": c.get("documentName"),
                    "docId": c.get("docId"),
                    "htmlContent": c.get("htmlContent"),
                })
        else:
            for tt in titles:
                if tt in k:
                    level = -1
                    break
            else:
                level = 1
            for c in v:
                res["inp_record"].append({
                    "level": level,
                    "title": c.get("documentName"),
                    "docId": c.get("docId"),
                    "htmlContent": c.get("htmlContent"),
                })
    res["inp_record"] = sorted(res["inp_record"], key=lambda t: t.get("level"))
    return res


@cache.memoize(timeout=7 * 24 * 60 * 60, make_name="_emr_fields_")
def get_case_fields(case_id, doc_name, table_name="emr"):
    collection = db.get_collection(table_name)
    info = collection.find_one({"caseId": case_id}, {"emr": 1})
    emr = info.get("emr") if info else {}
    res = []
    if doc_name == "病案首页":
        tmp = emr.get(doc_name) or []
        for t in tmp:
            content_list = parse_index(t.get("htmlContent"))
            res.extend(content_list)
    else:
        for _, v in emr.items():
            for c in v:
                if c.get("documentName") == doc_name:
                    res = parse_index(c.get("htmlContent"))
                    break
    return res


def parse_index(raw: str):
    """根据病案首页 html 原文, 将其转换为字典组成的列表, 每项包含 title, content, did, sid 四项"""
    if not raw:
        return []
    soup = BeautifulSoup(raw, 'lxml')
    spans = soup.find_all('span')
    rv = []
    for span in spans:
        title, did, sid, content = span.get('comment'), span.get('did'), span.get('sid'), span.text
        if title:
            rv.append({
                'title': title,
                'content': content,
                'did': did,
                'sid': sid
            })
    return rv


@cache.memoize(timeout=7 * 24 * 60 * 60, make_name="_emrx_html_")
def get_case_x(case_id):
    cursor = mysql.cursor()
    sql = "select caseId, docId, documentName, htmlContent from caseEmr where caseId='{}'".format(case_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    # wraps data
    buf = []
    for r in res:
        buf.append({
            "title": r[2],
            "docId": r[1],
            "htmlContent": r[3]
        })
    return buf

