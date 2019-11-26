#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2018/9/24'
"""
import json
from typing import Union

from .api_result import ApiResult
from .rabbit_mq_helper import RabbitMqHelper
from .redis_helper import RedisHelper


class ServiceUtility(object):

    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.redis_entity = RedisHelper()
        self.redis_connection = self.redis_entity.conn
        self.channel = RabbitMqHelper().connection.channel()

    def callback(self, ch, method, properties, body):
        req_id = ""
        req, resp = None, None

        try:
            req = json.loads(str(body, 'utf-8'))
            if not isinstance(req, dict):
                raise TypeError("invalid request data")

            req_id = req.get("id")
            req_param = req.get("param")
            if not req_id:
                raise ValueError("invalid request data, request id missing")
            if req_param is None:
                raise ValueError("invalid request data, params missing")

            resp = self.handle(req_param)

        except Exception as err:
            resp = ApiResult.failed(f'ERROR: {err}, request id:{req_id}')
        finally:
            if resp:
                self.redis_connection.setex(f'{self.redis_entity.key_prefix}://{req_id}',
                                            time=self.redis_entity.key_ttl,
                                            value=resp)
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def handle(self, message: Union[list, dict, str], service_name: str = "") -> ApiResult:
        raise NotImplementedError

    def start_consume(self):
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
        self.channel.start_consuming()
