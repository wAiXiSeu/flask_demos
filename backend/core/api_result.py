# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-10-14'
__description__ = doc description
"""
import json

from .http_response import ResultCode


class ApiResult(object):

    @staticmethod
    def success(data="", code=ResultCode.SUCCESS.value):
        return json.dumps({"code": code, "data": data}, ensure_ascii=False)

    @staticmethod
    def failed(message, code=ResultCode.BUSINESS_ERROR.value):
        return json.dumps({"code": code, "message": message}, ensure_ascii=False)
