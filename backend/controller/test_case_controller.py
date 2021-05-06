# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2021/4/29'
__description__ = doc description
"""

from flask import Blueprint, request

import service.test_case_service as service
from core.web_utils import api_response

test_case = Blueprint("test_case", __name__)


@test_case.route('/list', methods=["GET"])
def list_all_cases():
    hospital = request.args.get("hospital")
    return api_response(service.list_all_cases(hospital))


@test_case.route('/emr', methods=["POST"])
def get_emr():
    case_id = request.json.get("caseId")
    hospital = request.json.get("hospital")
    return api_response(service.get_emr(case_id, hospital))


@test_case.route("/qc", methods=["POST"])
def get_qc_result():
    case_id = request.json.get("caseId")
    return api_response(service.get_qc_result(case_id))
