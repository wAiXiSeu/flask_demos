# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-12-27'
__description__ = doc description
"""
import json
import os
from datetime import datetime

import redis

from core.exceptions import RedisError


class RedisHelper(object):
    def __init__(self, host, port, ttl=86400, prefix="simple"):
        self.host = os.getenv("REDIS_HOST", host)
        self.port = os.getenv("REDIS_PORT", port)
        self.key_ttl = os.getenv("REDIS_TTL", ttl)
        self.key_prefix = os.getenv("REDIS_PREFIX", prefix)
        self.conn = redis.Redis(host=self.host, port=self.port)

    def async_get_result(self, req_id, flag=None, time_out=600):
        """使用 request_id 在 redis 中获取结果
        Args:
            req_id: request id
            flag: 调用时给出调用者的名称
            time_out: 超时, 默认为一分钟
        Returns:
            list or dict, 正确的结果, 可以为空
        Raises:
            Exception: 超时或结果错误时抛出, 交由最初的调用者处理
        """
        start = datetime.now()
        now = datetime.now()
        result = None

        while not result and (now - start).seconds <= time_out:
            # TODO 此处会造成请求太多吗? Not async at all...
            result = self.conn.get(f"{self.key_prefix}://{req_id}")
            now = datetime.now()

        if (now - start).seconds > time_out:    # TODO 这个条件会成立吗
            raise RedisError(f"{flag}:{time_out}秒超时")
        try:
            result = json.loads(result)
            if not isinstance(result, dict):
                raise RedisError(f'result of rid {req_id} is not an instance of dict, result: {result}')
        except json.decoder.JSONDecodeError as e:
            raise RedisError(f"result decoder error when call json.loads.")
        return result
