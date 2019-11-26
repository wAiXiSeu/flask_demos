# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-10-12'
__description__ = doc description
"""
import json
from enum import Enum

from flask import Response


class ResultCode(Enum):
    SUCCESS = 0
    BUSINESS_ERROR = 2
    NOT_FINISHED = 3
    DB_ERROR = 4


class APIResponse(object):
    """成功或失败的返回, 包含两个静态方法, 指定 flask.Response 的数据,状态码和返回类型"""

    @staticmethod
    def success(data="", code=ResultCode.SUCCESS.value):
        return Response(
            json.dumps({'code': code, 'data': data}, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )

    @staticmethod
    def failed(message="", code=ResultCode.BUSINESS_ERROR.value):
        return Response(
            json.dumps({'code': code, 'message': message}, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )
