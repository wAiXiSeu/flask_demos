# coding: utf-8
# created by shijiliang on 2019-12-19

"""参数检查与获取函数
"""

from typing import Union

from .exceptions import FieldNotFound, FieldTypeError


def get_fields(param: dict,
               fields: Union[str, list],
               required: Union[str, list, bool] = None,
               as_dict: bool = False) -> Union[list, dict]:
    """获取参数, 用于从param中获取需要的字段
    Args:
        param: dict, 数据来源
        fields: str or list: 需要的字段, 列表或空格分隔的字符串
        required: str or list or bool, 必须要有的字段,为 True 时和 fields 一致,
                  对其进行非 None 检查, 为 None 则抛出异常
        as_dict: bool, 默认 False, 按 fields 的顺序返回列表, 设为 True 时返回字典
    Returns:
        dict if as_dict else list, 默认为 list 方便拆包, 若用于从字典中提取子项可将
        参数 as_dict 设为 True, 则返回字典
    Raises:
        FieldNotFound required 中的任一字段为 None 时抛出
    """
    if not isinstance(param, dict):
        raise FieldTypeError("param", dict, param)
    if isinstance(fields, str):
        fields = fields.split(' ')
    if required is True:
        required = fields
    if not required:
        required = []
    if isinstance(required, str):
        required = required.split(' ')

    resp = {} if as_dict else []
    for field in fields:
        value = param.get(field)
        if value is None and field in required:
            raise FieldNotFound(field=field)
        if as_dict:
            resp[field] = value
        else:
            resp.append(value)
    return resp


def check_fields(param: dict, fields: Union[str, list], types: list = None):
    if isinstance(fields, str):
        fields = fields.split(' ')
    if types and len(types) != len(fields):
        raise LookupError("length of fields not equal to check types.")
    for index, field in enumerate(fields):
        if param.get(field) is None:
            raise FieldNotFound(field=field)
        if types and not isinstance(param.get(field), types[index]):
            raise FieldTypeError(field, types[index], param.get(field))

