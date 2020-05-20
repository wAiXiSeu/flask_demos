# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020-05-20'
__description__ = doc description
"""
import os

from flask_caching import Cache


def prepare_config():
    if os.getenv("REDIS_HOST") and os.getenv("REDIS_PORT"):
        config = {
            'CACHE_TYPE': 'redis',
            'CACHE_REDIS_HOST': os.getenv("REDIS_HOST"),
            'CACHE_REDIS_PORT': os.getenv("REDIS_PORT"),
            'CACHE_DEFAULT_TIMEOUT': 12 * 60 * 60,
            'CACHE_KEY_PREFIX': "flask_demo_"
        }
    else:
        config = {'CACHE_TYPE': 'simple'}
    return config


cache = Cache(config=prepare_config())


def init(app):
    cache.init_app(app)
