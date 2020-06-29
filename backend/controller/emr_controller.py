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
from service.emr_service import get_emr_list, get_by_id, get_basic_info

emr = Blueprint("emr", __name__)


@emr.route("/list", methods=["GET", "POST"])
def list_emr():
    res = get_emr_list()
    return api_response(res)


@emr.route("/basic", methods=["GET", "POST"])
def get_basic():
    res = get_basic_info(request.args.get("caseId"))
    return api_response(res)


@emr.route("/case", methods=["GET", "POST"])
def get_emr():
    res = get_by_id(request.args.get("caseId"), {})
    return api_response(res)



