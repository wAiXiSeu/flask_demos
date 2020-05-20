# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-09-27'
__description__ = doc description
"""

from backend.core.web_utils import create_app, api_response
from controller.docker_controller import docker_operates
from controller.qc_debug_controller import qc_debug
from core.cache import init as cache_init

app = create_app()
cache_init(app)
app.register_blueprint(docker_operates, url_prefix="/docker")
app.register_blueprint(qc_debug, url_prefix="/qc")


@app.route("/ping", methods=["GET", "POST"])
def index():
    return api_response("pong!")


if __name__ == '__main__':
    app.run(host="localhost", port=12345, debug=True, load_dotenv=True)
