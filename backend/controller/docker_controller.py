# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-11-22'
__description__ = doc description
"""

from flask import Blueprint, request

from core.exceptions import ResultCode
from core.web_utils import api_response
from service.docker_service import list_docker_images, delete_docker_images

docker_operates = Blueprint("docker_ops", __name__)


@docker_operates.route("/images/list", methods=["GET"])
def list_images():
    images = list_docker_images()
    return api_response(images)


@docker_operates.route("/images/delete", methods=["POST"])
def delete_images():
    image_id = request.json.get("imageId")
    res = delete_docker_images(image_id)
    if not res:
        return api_response()
    else:
        return api_response(res, code=ResultCode.BUSINESS_ERROR.value)

