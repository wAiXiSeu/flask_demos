# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-12-27'
__description__ = doc description
"""

from traceback import format_exc

from flask import Flask, Response, jsonify
from flask_cors import CORS

from backend.core import loggers
from .exceptions import _BaseException, ResultCode
from .loggers import FlaskLogger


def api_response(result=None, code=ResultCode.SUCCESS.value, message='OK') -> Response:
    """标准返回格式, 正常返回时在 result 中附上数据, 有 warning 或错误时在 message 中附上消息.
    若传入的 result 是包含 code 和 message 属性的实例(自定义的Exception), 则优先使用 result 生成返回
    """
    if hasattr(result, 'code') and hasattr(result, 'message'):
        return jsonify({
            'code': result.code,
            'data': [],
            'message': result.message if result.message is not None else ''
        })
    return jsonify({
        'code': code,
        'data': result if result is not None else [],
        'message': message if message is not None else ''
    })


def exception_init(app):
    """全局异常处理, 若为可预见的异常, 即为 _BaseException 的子类时, 返回对应信息, 否则以 50000 为代码返回,
    堆栈放在 result 中, 既然只有 POST 没有其他的, 那状态码也就只有 200 吧, 具体情况看 code 的前三位即可"""

    @app.errorhandler(Exception)
    def handle_exception(error):
        FlaskLogger.log_error(error)
        if isinstance(error, _BaseException):
            return jsonify({
                'code': error.code,
                'data': [],
                'message': f'error: {error.message}',
                'trace_back': format_exc().split('\n')
            })
        else:
            return jsonify({
                'code': ResultCode.BUSINESS_ERROR.value,
                'data': [],
                'message': f'error: {error}',
                'trace_back': format_exc().split('\n')
            })


def create_app():
    """使用服务实例创建 flask app 实例, 调用服务实例的 handle 方法, 若 fields 参数不为空, 则进行参数字段检查"""
    app = Flask(__name__)
    exception_init(app)
    CORS(app, supports_credentials=True)
    loggers.init(app)

    @app.after_request
    def _after_request(resp):
        FlaskLogger.log_info(resp)
        return resp

    return app



