# coding: utf-8
# created by shijiliang on 2019-12-17

"""异常类,拥有 code 和 message 两个属性, 方便转换为标准返回格式
其中 code 为 int, 分为 400XX 和 500XX 两类, 分别对应客户端异常和服务端异常,
可自行添加, 01 ~ 99.
而 message 字段必须包括简短且精确的描述, 必要时附上 stack_trace.
"""

import json

from enum import unique, Enum


@unique
class ResultCode(Enum):
    """定义出现的返回码"""
    SUCCESS = 20000
    SUCCESS_WITH_BLANK_DATA = 20001

    REQUEST_DATA_NOT_FOUND = 40001
    FIELD_NOT_FOUND = 40002
    FIELD_TYPE_ERROR = 40003

    BUSINESS_ERROR = 50000
    REDIS_ERROR = 50001
    MQ_ERROR = 50002
    MODEL_ERROR = 50003
    HTTP_ERROR = 50004
    UNEXPECTED_ERROR = 50099


class _BaseResult(object):
    """
    正常返回结果基类
    """

    def __init__(self, code, data, message):
        self.code = code
        self.data = data
        self.message = message

    def __repr__(self):
        return f"{{code={self.code}, message={self.message})}}"

    def __str__(self):
        return json.dumps(self.dict, ensure_ascii=False)

    @property
    def dict(self):
        return self.__dict__

    def __getattr__(self, item):
        if item in self.dict:
            return self.dict[item]


class _BaseException(Exception):
    """错误基类"""

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __repr__(self):
        return f"{{code={self.code}, message={self.message})}}"

    def __str__(self):
        return json.dumps(
            {'code': self.code, 'data': [], 'message': self.message},
            ensure_ascii=False
        )

    def __getattr__(self, item):
        if item in self.dict:
            return self.dict[item]


class ClientException(_BaseException):
    """400 错误, 即调用者的问题, 其子类 code 前三位为 400"""
    pass


class ServerException(_BaseException):
    """500 错误, 即服务端的问题, 其子类 code 前三位为 500"""
    pass


# --- 200 ---

class Success(_BaseResult):
    """ 带有body的返回结果 """

    def __init__(self, data, message="OK"):
        super(Success, self).__init__(
            code=ResultCode.SUCCESS.value,
            data=data,
            message=message
        )


# --- 400 ---


class RequestDataNotFound(ClientException):
    """无法从请求中获取 json 数据时抛出此异常,
    http 时是无 request.json, mq 时是无法将从队列中获取的数据转为 json
    """

    def __init__(self):
        super(RequestDataNotFound, self).__init__(
            code=ResultCode.REQUEST_DATA_NOT_FOUND.value,
            message='cannot parse request data to json dict'
        )


class FieldNotFound(ClientException):
    """无法从请求数据中获取必须的字段时抛出此异常"""

    def __init__(self, field, type_=None):
        """Args:
        field: str, 字段名
        type_: str, 期望的类型
        """
        message = f"{self.__class__.__name__}: required field " \
            f"`{field}{': ' + type_ if type_ else ''}` not found"
        super(FieldNotFound, self).__init__(
            code=ResultCode.FIELD_NOT_FOUND.value,
            message=message
        )


class FieldTypeError(ClientException):
    """请求数据中某字段类型不正确时抛出此异常"""

    def __init__(self, field, type_, value):
        """Args:
        field: str, 字段名
        type_: str, 字段期望类型
        value: 在请求中实际获取到的此字段的数据
        """
        super(FieldTypeError, self).__init__(
            code=ResultCode.FIELD_TYPE_ERROR.value,
            message=f"{self.__class__.__name__}: field {field} "
            f"expected {type_}, not {value}:{type(value)}"
        )


# --- 500 ---

class BusinessError(ServerException):
    """
    服务端通用业务异常
    """
    def __init__(self, e):
        super(BusinessError, self).__init__(
            code=ResultCode.BUSINESS_ERROR.value,
            message=f"{self.__class__.__name__}: {e}"
        )


class RedisError(ServerException):
    """Redis 发生错误时抛出此异常, e 为字符串或某异常, 当为异常实例时
    使用 f-string 相当于 str(e)"""

    def __init__(self, e):
        super(RedisError, self).__init__(
            code=ResultCode.REDIS_ERROR.value,
            message=f"{self.__class__.__name__}: {e}"
        )


class MQError(ServerException):
    """MQ 发生错误时抛出此异常, e 为字符串或某异常, 当为异常实例时
    使用 f-string 相当于 str(e)"""

    def __init__(self, e):
        super(MQError, self).__init__(
            code=ResultCode.MQ_ERROR.value,
            message=f"{self.__class__.__name__}: {e}"
        )


class ModelError(ServerException):
    """模型服务发生错误时抛出此异常, e 为字符串或某异常, 当为异常实例时
    使用 f-string 相当于 str(e)"""

    def __init__(self, e):
        super(ModelError, self).__init__(
            code=ResultCode.MODEL_ERROR.value,
            message=f"{self.__class__.__name__}: {e}"
        )


class HTTPError(ServerException):
    """
    HTTP 调用第三方服务时抛出的异常
    """

    def __init__(self, e):
        super(HTTPError, self).__init__(
            code=ResultCode.HTTP_ERROR.value,
            message=f"{self.__class__.__name__}: {e}"
        )


class UnexpectedServerError(ServerException):
    """发生未预料到的错误时抛出此异常, e 为字符串或某异常,
    当为异常实例时使用 f-string 相当于 str(e),
    将 code 定为 50099 作为最后的异常"""

    def __init__(self, e):
        super(ServerException, self).__init__(
            code=ResultCode.UNEXPECTED_ERROR.value,
            message=f"{self.__class__.__name__}: {type(e)}: {e}"
        )
