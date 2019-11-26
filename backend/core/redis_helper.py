#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2018/9/21'
"""
import json
import os
from datetime import datetime
from traceback import print_exc

import redis

from .exceptions import BusinessException


class RedisHelper(object):
    def __init__(self):
        self.host = os.getenv("redis_host", "localhost")
        self.port = os.getenv("redis_port", 6379)
        self.key_ttl = os.getenv("redis_key_ttl", 200)
        self.key_prefix = os.getenv("redis_key_prefix", "model-response")
        self.conn = redis.Redis(host=self.host, port=self.port)

    def get_conn(self):
        return self.conn

    def async_get_result(self, req_id, flag=None, time_out=60):
        """使用 request_id 在 redis 中获取结果
        Args:
            req_id: request id
            flag: 调用时给出调用者的名称
            time_out: 超时, 默认为一分钟
        Returns:
            list or dict, 正确的结果, 可以为空
        Raises:
            BusinessException: 超时或结果错误时抛出, 交由最初的调用者处理
        """
        start = datetime.now()
        now = datetime.now()
        result = None
        while not result and (now - start).seconds <= time_out:
            # TODO 此处会造成请求太多吗? Not async at all...
            result = self.conn.get("{key_prefix}://{req_id}".format(key_prefix=self.key_prefix, req_id=req_id))
            now = datetime.now()
        try:
            if (now - start).seconds > time_out:    # TODO 这个条件会成立吗
                raise BusinessException("{flag}:{time_out}秒超时".format(flag=flag, time_out=time_out))
            result = json.loads(result)
            if type(result) == dict and result.get('err'):
                raise BusinessException(result.get('err'))
            else:
                return result
        except Exception as e:
            print_exc()
            raise BusinessException("{flag}错误，{error}, result: {result}".format(flag=flag, error=str(e), result=result))
