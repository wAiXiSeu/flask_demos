# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-12-27'
__description__ = doc description
"""
import os

import pika
from pika.exceptions import ConnectionWrongStateError

from backend.core.exceptions import MQError


class RabbitMqHelper:
    """适用于生产者和消费者"""
    def __init__(self, host, port, user=None, password=None, consumer=True):
        self.host = os.getenv("RABBIT_MQ_HOST", host)
        self.port = os.getenv("RABBIT_MQ_PORT", port)
        self.username = os.getenv("RABBIT_MQ_USERNAME", user)
        self.password = os.getenv("RABBIT_MQ_PASSWORD", password)
        cred = None
        if self.username and self.password:
            cred = pika.credentials.PlainCredentials(self.username, self.password)
        if not consumer:
            self.param = pika.ConnectionParameters(self.host, self.port, '/', credentials=cred, heartbeat=0)
        else:
            self.param = pika.ConnectionParameters(self.host, self.port, '/', credentials=cred, heartbeat=600,
                                                   blocked_connection_timeout=300, connection_attempts=120,
                                                   retry_delay=1)
        self.connection = pika.BlockingConnection(self.param)

    def get_channel(self, retry=5):
        if retry == 0:
            raise MQError(f'ConnectionWrongStateError occurred after trying to get channel for 5 times')
        try:
            return self.connection.channel()
        except ConnectionWrongStateError as e:
            print('ConnectionWrongStateError occurred , retry count left {}'.format(retry))
            # producer only
            self.connection = pika.BlockingConnection(self.param)
            return self.get_channel(retry-1)

    def publish(self, routing_key, message, queue_name='default-queue'):
        # todo 可以启用exchange
        channel = self.get_channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(exchange='', routing_key=routing_key, body=message)

