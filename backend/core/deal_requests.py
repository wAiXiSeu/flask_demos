# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-10-12'
__description__ = doc description
"""
import json
from typing import Union

import requests

from .logging import ThirdPartyLogger
from .exceptions import BusinessException


@ThirdPartyLogger.log_third_party()
def deal_request(url: str,
                 data: Union[str, dict, list] = "{}",
                 timeout: int = 20,
                 method: str = 'post') -> list:
    if method.upper() == 'POST':
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        if isinstance(data, str):
            result = requests.post(url, data=data.encode('utf-8'), headers=headers, timeout=timeout)
        elif isinstance(data, (list, dict)):
            result = requests.post(url, json=data)
        else:
            raise BusinessException('data should be an instance of list, dict or str')
    elif method.upper() == 'GET':
        result = requests.get(url, params=data, timeout=timeout)
    else:
        raise BusinessException('method not support.')
    if result.status_code != 200:
        raise BusinessException(result.text)
    result_js = json.loads(result.text)
    return result_js
