# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-09-27'
__description__ = doc description
"""
import time

from flask import Flask, request

from controller.docker_controller import docker_operates
from core.cors import init as init_cors
from core.exceptions import init as init_error
from core.http_response import APIResponse
from core.logging import FlaskLogger

app = Flask(__name__)
app.config["SECRET_KEY"] = "waixi hello world"
init_error(app)
init_cors(app)
app.register_blueprint(docker_operates, url_prefix="/docker")


@app.route("/ping", methods=["GET", "POST"])
def index():
    return APIResponse.success("pong!")


@app.before_request
def _before_request(*args, **kwargs):
    start_time = time.time()
    request.start_time = start_time


@app.after_request
def _after_request(response):
    cost_time = time.time() - request.start_time
    FlaskLogger.log_info(response, cost_time=cost_time)
    return response


if __name__ == '__main__':
    app.run(host="localhost", port=12345, debug=True)
