# coding: utf-8
# created by shijiliang on 2019-12-17

"""常用装饰器
"""

from datetime import datetime
from functools import wraps


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = datetime.now()
        resp = func(*args, **kwargs)
        cost = (datetime.now() - t0).total_seconds()
        info = f'timeit: total time cost of `{func.__name__}` is {cost}s'
        print(info)
        return resp
    return wrapper
