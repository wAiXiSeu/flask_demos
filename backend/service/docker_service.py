# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-10-12'
__description__ = doc description
"""
import datetime

import docker

from core.exceptions import BusinessError

docker_client = docker.from_env()


def list_docker_images():
    images = docker_client.images.list()
    res = []
    for t in images:
        info = dict()
        info["id"] = t.id
        info["tags"] = t.tags
        info["container"] = t.attrs.get("Container")
        create_time = datetime.datetime.strptime(t.attrs.get("Created").split(".")[0], "%Y-%m-%dT%H:%M:%S")
        info["created"] = str(create_time)
        now_utc = datetime.datetime.strptime(
            datetime.datetime.strftime(datetime.datetime.now(datetime.timezone.utc), "%Y-%m-%dT%H:%M:%S"),
            "%Y-%m-%dT%H:%M:%S")
        info["since"] = (now_utc-create_time).days
        info["size"] = round(t.attrs.get("Size") / (1024*1024*1024), 4)
        res.append(info)
    return sorted(res, key=lambda s: s.get("size") or 0, reverse=True)


def delete_docker_images(image_id):
    if not image_id:
        raise BusinessError("镜像ID为空")
    try:
        docker_client.images.remove(image_id)
    except Exception as e:
        return str(e)
    return ""
