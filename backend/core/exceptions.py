# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-10-12'
__description__ = doc description
"""
from flask import jsonify

from .http_response import ResultCode
from .logging import FlaskLogger


class BusinessException(Exception):
    def __init__(self, message, code=ResultCode.BUSINESS_ERROR.value):
        self.code = code
        self.message = message


class DBException(Exception):
    def __init__(self, message, code=ResultCode.DB_ERROR.value):
        self.code = code
        self.message = message


def init(app):
    """确保出现错误时返回指定格式的 json, 而非 html"""
    @app.errorhandler(Exception)
    def handle_exception(error):
        status_code = 500
        if isinstance(error, BusinessException):
            status_code = 200
        FlaskLogger.log_error(error)
        return jsonify({
            'code': error.code if hasattr(error, 'code') else ResultCode.BUSINESS_ERROR.value,
            'message': str(error)
        }), status_code
