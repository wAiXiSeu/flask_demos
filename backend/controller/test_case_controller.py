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


@test_case.route('/emr', methods=["GET"])
def get_emr():
    case_id = request.args.get("caseId")
    hospital = request.args.get("hospital")
    return api_response(service.get_emr(case_id, hospital))


@test_case.route("/qc", methods=["GET"])
def get_qc_result():
    case_id = request.args.get("caseId")
    return api_response(service.get_qc_result(case_id))


@test_case.route("/delete", methods=["POST"])
def delete_test_data():
    return api_response(service.delete_test_data())


@test_case.route("/download", methods=["GET"])
def download_test_data():
    return service.download_test_data()


@test_case.route("/doctor_result", methods=["GET"])
def get_doctor_result():
    case_id = request.args.get("caseId")
    qc_id = request.args.get("qcId")
    return api_response(service.get_doctor_result(case_id, qc_id))
