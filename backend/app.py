# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-09-27'
__description__ = doc description
"""
from flask_cors import CORS

from controller.tz_emr_controller import tz_emr
from core.web_utils import create_app, api_response
from controller.test_case_controller import test_case
from core.cache import init as cache_init

app = create_app()
cache_init(app)
CORS(app)
app.register_blueprint(test_case, url_prefix="/cases")
app.register_blueprint(tz_emr, url_prefix="/tz")


@app.route("/ping", methods=["GET", "POST"])
def index():
    return api_response("pong!")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=12345, debug=True, load_dotenv=True)
