# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2020-04-14'
__description__ = 数字相关工具
"""
import copy
import functools
import inspect


def text2number(text, target_type=float):
    try:
        return target_type(eval(text)) if isinstance(text, str) else text
    except Exception as e:
        raise ValueError("{} cannot be convert to a number.".format(text))


def check_number(fields=None):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            params = list(inspect.signature(func).parameters.keys())
            check_items = fields.split() if isinstance(fields, str) else fields or params
            arg_params = list(copy.deepcopy(args))
            for f in check_items:
                if f not in params:
                    raise LookupError("field {} not found in params.".format(f))
                idx = params.index(f)
                if f in kwargs:
                    kwargs[f] = text2number(kwargs.get(f), target_type=float)
                elif idx < len(arg_params):
                    arg_params[idx] = text2number(arg_params[idx], target_type=float)

            return func(*arg_params, **kwargs)
        return inner

    return wrapper

