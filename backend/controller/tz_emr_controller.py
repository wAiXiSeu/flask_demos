# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020/9/28'
__description__ = doc description
"""

from flask import Blueprint, request

from core.web_utils import api_response
from service.tz_emr_service import get_vid_list, get_doc_list, get_details

tz_emr = Blueprint("tz_emr", __name__)


@tz_emr.route("/vid", methods=["GET"])
def _list_vid():
    return api_response(get_vid_list())


@tz_emr.route("/doc", methods=["GET"])
def _list_doc():
    vid = request.args.get('vid')
    return api_response(get_doc_list(vid))


@tz_emr.route("/details", methods=["GET", "POST"])
def _list_details():
    vid = request.args.get('vid')
    doc = request.args.get('doc')
    return api_response(get_details(vid, doc))

