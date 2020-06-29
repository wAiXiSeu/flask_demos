# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-09-27'
__description__ = doc description
"""
from flask_cors import CORS

from core.web_utils import create_app, api_response
from controller.docker_controller import docker_operates
from controller.emr_controller import emr
from controller.qc_debug_controller import qc_debug
from controller.test_case_controller import test_case
from core.cache import init as cache_init

app = create_app()
cache_init(app)
CORS(app)
app.register_blueprint(docker_operates, url_prefix="/docker")
app.register_blueprint(qc_debug, url_prefix="/qc")
app.register_blueprint(test_case, url_prefix="/cases")
app.register_blueprint(emr, url_prefix="/syf")


@app.route("/ping", methods=["GET", "POST"])
def index():
    return api_response("pong!")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=12345, debug=True, load_dotenv=True)
