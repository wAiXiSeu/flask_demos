# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020-06-12'
__description__ = doc description
"""

from flask import Blueprint, request

from core.exceptions import ResultCode
from core.web_utils import api_response
import service.test_case_service as service

test_case = Blueprint("test_case", __name__)


@test_case.route("/list", methods=["GET"])
def list_cases():
    return api_response(service.list_cases())


@test_case.route("/upsert", methods=["POST"])
def upsert_cases():
    return api_response(service.upsert_cases(request.get_json()))


@test_case.route("/delete", methods=["POST"])
def delete_cases():
    return api_response(service.delete_cases(request.get_json()))
