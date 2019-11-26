#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2018/9/21'
"""
import os

import pika
from pika.exceptions import StreamLostError


class RabbitMqHelper:
    def __init__(self):
        self.host = os.getenv('rabbitmq_host', '192.168.80.20')
        self.port = os.getenv('rabbitmq_port', 30072)
        self.username = os.getenv("rabbitmq_user", "rxthinking")
        self.password = os.getenv("rabbitmq_password", "gniknihtxr")
        self.cred = None
        if self.username and self.password:
            self.cred = pika.credentials.PlainCredentials(self.username, self.password)


class RabbitPublisher(RabbitMqHelper):
    def __init__(self):
        super(RabbitPublisher, self).__init__()
        self.param = pika.ConnectionParameters(self.host, self.port, '/', credentials=self.cred, heartbeat=0,
                                               connection_attempts=120, retry_delay=1)
        self.connection = pika.BlockingConnection(self.param)

    def get_channel(self):
        try:
            return self.connection.channel()
        except StreamLostError as e:
            self.connection = pika.BlockingConnection(self.param)
            return self.connection.channel()

    def publish(self, routing_key, message, queue_name='test'):
        channel = self.get_channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(exchange='', routing_key=routing_key, body=message)


class RabbitConsumer(RabbitMqHelper):
    def __init__(self):
        super(RabbitConsumer, self).__init__()
        self.param = pika.ConnectionParameters(self.host, self.port, '/', credentials=self.cred, heartbeat=600,
                                               connection_attempts=120, retry_delay=1)
        self.connection = pika.BlockingConnection(self.param)

    def get_channel(self):
        try:
            return self.connection.channel()
        except Exception as e:
            self.connection = pika.BlockingConnection(self.param)
            return self.connection.channel()

    def consume(self, queue_name, callback):
        if not callable(callback):
            raise TypeError("consumer callback type error.")
        channel = self.get_channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        channel.start_consuming()
