# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-11-22'
__description__ = doc description
"""

from flask import Blueprint, request

from core.http_response import APIResponse
from service.docker_service import list_docker_images, delete_docker_images

docker_operates = Blueprint("docker_ops", __name__)


@docker_operates.route("/images/list", methods=["GET"])
def list_images():
    images = list_docker_images()
    return APIResponse.success(images)


@docker_operates.route("/images/delete", methods=["POST"])
def delete_images():
    image_id = request.json.get("imageId")
    res = delete_docker_images(image_id)
    if not res:
        return APIResponse.success()
    else:
        return APIResponse.failed(res)

