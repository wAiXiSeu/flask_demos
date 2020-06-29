# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020-06-29'
__description__ = doc description
"""
from core.db.mongo_helper import MongoHelper

collection = MongoHelper("localhost", 27017, "syf_example").get_collection("emr")


def get_emr_list():
    return list(collection.distinct("caseId"))


def get_basic_info(case_id):
    info = collection.find_one({"caseId": case_id}, {"emr": 0, "_id": 0})
    return dict(info)


def get_by_id(case_id, filters):
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
                    "content": c.get("htmlContent")
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
                    "content": c.get("htmlContent")
                })
    res["inp_record"] = sorted(res["inp_record"], key=lambda t: t.get("level"))
    return res
