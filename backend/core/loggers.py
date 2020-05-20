# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-12-30'
__description__ = doc description
"""
import datetime
import functools
import inspect
import json
import logging
import os
import threading
import time
import traceback
from functools import wraps
from logging import handlers, config
from stat import ST_DEV, ST_INO

from flask import request

root_dir = os.getenv("ROOT_DIR") or os.path.join(os.path.dirname(__file__), "..")
sub_dir = os.getenv('HOSTNAME') or datetime.datetime.now().strftime("%Y%m%d")
custom_log_dir = os.path.join(root_dir, "logs", sub_dir)


def init(app):
    """整合 flask 与 gunicorn 的 logger"""
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(logging.DEBUG)
    # 加一个日志
    with threading.Lock():
        if not os.path.exists(custom_log_dir):
            os.makedirs(custom_log_dir)


class TimeCostLogger(object):
    """
    时间花费装配器, 默认输出console 和 file
    """

    @staticmethod
    def time_cost(where: str):
        def _wraps(func):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                start = time.time()
                res = func(*args, **kwargs)
                cost = time.time() - start
                get_logger("simple").info(json.dumps({
                    "message_type": "rxTIME",
                    "where": where,
                    "cost": cost
                }, ensure_ascii=False))
                return res

            return inner

        return _wraps


class LocalLogger(object):
    """
    本地debug error 信息日志，输出默认为console 和 file
    """

    @staticmethod
    def debug(msg, msg_type="rxDEBUG", **kwargs):
        """代码中可用此函数 debug, 代替 print"""
        where = kwargs.pop("where") if "where" in kwargs else ""
        get_logger("root").debug(json.dumps({
            "message_type": msg_type,
            "message": msg,
            "where": where,
            "custom_params": kwargs
        }, ensure_ascii=False))

    @staticmethod
    def error(error, msg_type="rxERROR", **kwargs):
        where = kwargs.pop("where") if "where" in kwargs else ""
        get_logger("error").error(json.dumps({
            "message_type": msg_type,
            "error_message": str(error),
            "where": where,
            "custom_params": kwargs,
            "error_stack": traceback.format_exc()
        }, ensure_ascii=False))

    @staticmethod
    def info(response, msg_type="rxINFO", **kwargs):
        logger = get_logger("simple")
        where = kwargs.pop("where") if "where" in kwargs else ""
        message = {
            "message_type": msg_type,
            "message": response,
            "where": where,
            "custom_params": kwargs
        }
        logger.info(json.dumps(message, ensure_ascii=False))


class ThirdPartyLogger(object):
    """
    第三方调用日志记录，默认输出file
    *kwargs:
        *url
        *method
        *params
        *message_type
        *cost_time [optional]
    """

    @staticmethod
    def log_info(response, log_name="simple", **kwargs):
        logger = get_logger(log_name)
        url = kwargs.pop("url") if "url" in kwargs else ""
        method = kwargs.pop("method") if "method" in kwargs else ""
        params = kwargs.pop("params") if "params" in kwargs else ""
        cost_time = kwargs.pop("cost_time") if "cost_time" in kwargs else ""
        message_type = kwargs.pop("message_type") if "message_type" in kwargs else "third_party"
        message = {
            "message_type": message_type,
            "third_url": url,
            "third_method": method,
            "third_params": params,
            "third_results": response,
            "cost_time(seconds)": cost_time
        }
        logger.info(json.dumps(message, ensure_ascii=False))

    @staticmethod
    def log_error(error, log_name="error", **kwargs):
        logger = get_logger(log_name)
        url = kwargs.pop("url") if "url" in kwargs else ""
        method = kwargs.pop("method") if "method" in kwargs else ""
        params = kwargs.pop("params") if "params" in kwargs else ""
        message_type = kwargs.pop("message_type") if "message_type" in kwargs else "third_party"
        message = {
            "message_type": message_type,
            "third_url": url,
            "third_method": method,
            "third_params": params,
            "third_exception_type": type(error).__name__,
            "third_exception_msg": str(error)
        }
        logger.error(json.dumps(message, ensure_ascii=False))

    @staticmethod
    def log_third_party(log_name="simple", message_type="third_party"):
        def do_log(func):
            @wraps(func)
            def inner(*args, **kwargs):
                arg_names = inspect.getfullargspec(func).args
                defaults = inspect.getfullargspec(func).defaults or ""
                params = {k: v for k, v in zip(arg_names, [*args, *defaults])}
                params.update(kwargs)
                if "self" in params:
                    params.pop("self")
                url = params.pop("url") if "url" in params else ""
                method = params.pop("method") if "method" in params else ""
                try:
                    start = time.time()
                    result = func(*args, **kwargs)
                    try:
                        to_log = json.loads(result)
                    except:
                        to_log = str(result)
                    cost_time = time.time() - start
                    ThirdPartyLogger.log_info(to_log, log_name, url=url, method=method, params=params,
                                              cost_time=cost_time, message_type=message_type)
                    return result
                except Exception as e:
                    ThirdPartyLogger.log_error(e, log_name, url=url, method=method, params=params,
                                               message_type=message_type)
                    raise e

            return inner

        return do_log


class FlaskLogger(object):
    """
    flask日志记录 默认输出file
    """

    @staticmethod
    def log_info(response, log_name="simple", **kwargs):
        cost_time = kwargs.pop("cost_time") if "cost_time" in kwargs else ""
        logger = get_logger(log_name)
        if response.status_code == 200:
            message = {
                "message_type": "rxINFO",
                'request_path': request.path,
                'request_remote_addr': request.remote_addr,
                'request_method': request.method,
                'request_params': str(request.query_string, 'utf-8') if request.query_string else str(request.data,
                                                                                                      'utf-8'),
                "status_code": response.status_code,
                "response_data": json.loads(response.data) if response.content_type == "application/json" else "",
                "cost_time(seconds)": cost_time
            }
            logger.info(json.dumps(message, ensure_ascii=False))

    @staticmethod
    def log_error(error, log_name="error", **kwargs):
        logger = get_logger(log_name)
        message = {
            "message_type": "rxERROR",
            'request_path': request.path,
            'request_remote_addr': request.remote_addr,
            "request_method": request.method,
            'request_params': str(request.query_string, 'utf-8') if request.query_string else str(request.data,
                                                                                                  'utf-8'),
            'exception_type': type(error).__name__,
            'error_message': str(error),
            "error_stack": traceback.format_exc()
        }
        logger.error(json.dumps(message, ensure_ascii=False))


class RxLogHandler(handlers.WatchedFileHandler, handlers.TimedRotatingFileHandler):
    def __init__(self, filename, when='D', interval=1, backupCount=7, encoding="utf8"):
        handlers.TimedRotatingFileHandler.__init__(self, filename=filename, when=when, interval=interval,
                                                   backupCount=backupCount, encoding=encoding)
        self.dev, self.ino = -1, -1
        self._statstream()

    def _open(self):
        dir_name = os.path.dirname(self.baseFilename)
        with threading.Lock():
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
        return handlers.TimedRotatingFileHandler._open(self)

    def emit(self, record):
        """
        Emit a record.

        If underlying file has changed, reopen the file before emitting the
        record to it.
        """
        try:
            # stat the file by path, checking for existence
            sres = os.stat(self.baseFilename)
        except FileNotFoundError:
            sres = None
        # compare file system stat with that of our stream file handle
        if not sres or sres[ST_DEV] != self.dev or sres[ST_INO] != self.ino:
            if self.stream is not None:
                # we have an open file handle, clean it up
                self.stream.flush()
                self.stream.close()
                self.stream = None  # See Issue #21742: _open () might fail.
                # open a new file handle and get new stat info from that fd
                self.stream = self._open()
                self._statstream()
        handlers.TimedRotatingFileHandler.emit(self, record)


class RxLogFormatter(logging.Formatter):
    def __init__(self):
        fmt = "%(asctime)s - [%(message_type)s] - %(levelname)s - %(message)s"
        super(RxLogFormatter, self).__init__(fmt=fmt)

    def format(self, record):
        try:
            msg = json.loads(record.getMessage())
            typo = msg.pop("message_type") if "message_type" in msg else ""
            record.__dict__["message_type"] = typo
        except Exception as e:
            record.__dict__["message_type"] = ""
        return super(RxLogFormatter, self).format(record)


def get_logger(name):
    return logging.getLogger(name)


logger_config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(process)d - %(levelname)s - %(message)s',
        },
        'rx_formatter': {
            '()': RxLogFormatter,
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': os.environ.get("LOG_LEVEL", "DEBUG").upper(),
            'formatter': 'rx_formatter'
        },
        'log_handler': {
            '()': RxLogHandler,
            'formatter': 'rx_formatter',
            'filename': os.path.join(custom_log_dir, "operations.log"),
            'level': os.environ.get("LOG_LEVEL", "DEBUG").upper(),
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'simple': {
            'handlers': ['log_handler'],
            'level': 'DEBUG',
        },
        'error': {
            'handlers': ['log_handler', 'console'],
            'level': 'ERROR',
        }
    }
}

logging.config.dictConfig(logger_config)
