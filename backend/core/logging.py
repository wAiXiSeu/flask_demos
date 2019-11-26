# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-11-16'
__description__ = doc description
"""
import functools
import inspect
import json
import logging
import os
import time
import traceback
from functools import wraps
from logging import handlers, config
from stat import ST_DEV, ST_INO

from flask import request

custom_log_dir = os.path.join(os.getenv("LOG_DIR", "./logs"))


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
                get_logger("debug_info").info(json.dumps({
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
    def debug(msg, msg_type="rxDEBUG"):
        """代码中可用此函数 debug, 代替 print"""
        get_logger("debug_info").debug(json.dumps({
            "message_type": msg_type,
            "message": msg
        }, ensure_ascii=False))

    @staticmethod
    def error(error, msg_type="rxERROR"):
        get_logger("debug_info").debug(json.dumps({
            "message_type": msg_type,
            "error_message": str(error),
            "error_stack": traceback.format_exc()
        }, ensure_ascii=False))


class MiddleWareLogger(object):
    """
    中间件日志记录，e.g. redis rabbitmq 默认输出 file
    """
    @staticmethod
    def log_info(response, log_name="simple", **kwargs):
        logger = get_logger(log_name)
        params = kwargs.pop("params") if "params" in kwargs else ""
        cost_time = kwargs.pop("cost_time") if "cost_time" in kwargs else ""
        message_type = kwargs.pop("message_type") if "message_type" in kwargs else "redis"
        message = {
            "message_type": message_type,
            "params": params,
            "results": response,
            "cost_time(seconds)": cost_time
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
    def log_error(error, log_name="simple", **kwargs):
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
    def log_error(error, log_name="simple", **kwargs):
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
        dir_path = os.path.dirname(self.baseFilename)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
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
            'level': os.environ.get("LOG_LEVEL", "INFO").upper(),
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
        "debug_info": {
            'handlers': ['console', 'log_handler'],
            'level': 'DEBUG',
        }
    }
}

logging.config.dictConfig(logger_config)
