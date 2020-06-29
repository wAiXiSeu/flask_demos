# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020-06-29'
__description__ = doc description
"""
from pymongo import MongoClient

from core.cache import cache

db = MongoClient(host="mongo", port=27017).get_database("syf_example")


def get_emr_list(collection_name):
    collection = db.get_collection(collection_name)
    return list(collection.distinct("caseId"))


def get_basic_info(case_id, table_name="emr"):
    collection = db.get_collection(table_name)
    info = collection.find_one({"caseId": case_id}, {"emr": 0, "_id": 0})
    return dict(info)


@cache.memoize(timeout=7*24*60*60, make_name="_emr_html_")
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


@cache.memoize(timeout=7*24*60*60, make_name="_emr_fields_")
def get_case_fields(case_id, doc_name, table_name="emr"):
    collection = db.get_collection(table_name)
    info = collection.find_one({"caseId": case_id}, {"emr": 1})
    emr = info.get("emr") if info else {}
    res = []
    if doc_name == "病案首页":
        tmp = emr.get(doc_name) or []
        for t in tmp:
            res.extend(t.get("contents"))
    else:
        for _, v in emr.items():
            for c in v:
                if c.get("documentName") == doc_name:
                    res = c.get("contents")
                    break
    return res
