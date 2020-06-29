# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020-06-29'
__description__ = doc description
"""
from flask import Blueprint, request

from core.web_utils import api_response
from service.emr_service import get_emr_list, get_by_id, get_basic_info, get_case_fields

emr = Blueprint("emr", __name__)


@emr.route("/list", methods=["GET", "POST"])
def _list_emr():
    table = request.get_json().get("collection_name")
    res = get_emr_list(table)
    return api_response(res)


@emr.route("/basic", methods=["GET", "POST"])
def _get_basic():
    res = get_basic_info(request.args.get("caseId"), request.args.get("collection_name"))
    return api_response(res)


@emr.route("/case", methods=["GET", "POST"])
def _get_emr():
    res = get_by_id(request.args.get("caseId"), {}, request.args.get("collection_name"))
    return api_response(res)


@emr.route("/fields", methods=["GET", "POST"])
def _get_case_fields():
    res = get_case_fields(request.args.get("caseId"), request.args.get("docName"),  request.args.get("collection_name"))
    return api_response(res)

