# coding: utf-8
# created by shijiliang on 2020-01-04

"""加密工具
"""

from hashlib import md5 as _md5
from os import getenv

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

SECRET_KEY = getenv('SECRET_KEY') or 'zs9UAsrb'


def md5(s: str):
    m = _md5()
    m.update(s.encode())
    return m.hexdigest()


def serialize(dic: dict):
    serializer = Serializer(secret_key=SECRET_KEY, expires_in=86400)
    return serializer.dumps(dic).decode('utf-8')


def deserialize(s: str):
    serializer = Serializer(secret_key=SECRET_KEY, expires_in=86400)
    try:
        return serializer.loads(s.encode('utf-8'))
    except:
        return None
