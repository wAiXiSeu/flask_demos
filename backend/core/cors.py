# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-11-22'
__description__ = doc description
"""
from flask_cors import CORS


def init(app):
    CORS(app, supports_credentials=True)
