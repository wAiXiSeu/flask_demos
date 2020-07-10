# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-10-12'
__description__ = doc description
"""

"""gunicorn 默认配置文件
将所有的配置放置于此, 在启动服务时使用
`gunicorn app:app` 可自动读取此文件并应用配置

所有的配置选项参见 http://docs.gunicorn.org/en/stable/settings.html
"""

bind = '0.0.0.0:12345'

# 进程数
workers = 1

# 线程数
# threads = 2

# 保持默认 sync
worker_class = 'gevent'

# 日志等级, 调试时可改为 debug
loglevel = 'debug'

# 将访问日志和错误日志输出到控制台
accesslog = '-'
errorlog = '-'

preload = True
