# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020-05-20'
__description__ = doc description
"""
from flask import Blueprint

import service.qc_debug_service as service
from core.web_utils import api_response

qc_debug = Blueprint("qc", __name__)


@qc_debug.route("/get/<rid>", methods=["GET"])
def search_logs(rid: str):
    res = service.get_logs(rid)
    return api_response(res)

