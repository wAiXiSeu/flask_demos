# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020-04-13'
__description__ = singleton
"""
import threading


class Singleton(type):
    """
    :usage
        [py3]
        class Person(metaclass=Singleton):
            def __init__(self, description="I am a person"):
                self.description = description
    """
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with Singleton._lock:
            if not hasattr(cls, "_instance"):
                cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance
