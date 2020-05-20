#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-03-07'
__description__ = 正则工具 py3
"""
import re
from collections import defaultdict


def find_chinese(text):
    """
    判断 text 是否包含中文，如果包含，返回所有中文
    :param text:
    :return:
    """
    for t in text:
        if u'\u4E00' <= t <= u'\u9FFF':
            pattern = re.compile("[\u4E00-\u9FFF]+")
            result = re.findall(pattern, text)
            return True, result
    return False, ''


def find_num(text):
    """
    判断 text 是否包含数字，如果包含，返回所有数字
    :param text:
    :return:
    """
    for t in text:
        if u'\u0030' <= t <= u'\u0039':
            pattern = re.compile("[\u0030-\u0039]+")
            result = re.findall(pattern, text)
            return True, result
    return False, ''


def deal_auto_set(stats_set):
    def _find_chinese(text):
        """
        判断 text 是否包含中文，如果包含，返回所有中文
        :param text:
        :return:
        """
        for t in text:
            if u'\u4E00' <= t <= u'\u9FFF':
                pattern = re.compile("[\u4E00-\u9FFF]+")
                result = re.findall(pattern, text)
                return True, result
        return False, ''

    result = set()
    items = defaultdict(int)
    for txt in stats_set:
        status, part = _find_chinese(txt)
        if status:
            items[part[0]] += 1
        else:
            result.add(txt)
    for k, v in items.items():
        v = v * 2 if v > 10 else 10
        for i in range(v):
            result.add('{}{}'.format(k, i))
    return sorted(result)


if __name__ == '__main__':
    s = """,
:
;
.
?
!
PE
PS
U
，
；
：
！
？
。
体液123性质0
体液性质1
体液性质2
医学耗材0
医学耗材1
医学耗材2
否定0
否定1
否定10
否定2
否定3
否定4
否定5
否定6
否定7
否定8
否定9
实体结果0
实体结果1
实体结果10
实体结果11
实体结果12
实体结果13
实体结果14
实体结果15
实体结果16
实体结果17
实体结果2
实体结果3
实体结果4
实体结果5
实体结果6
实体结果7
实体结果8
实体结果9
形态0
形态1
形态2
形态3
形状0
形状1
形状2
形状3
数目0
数目1
数目2
数目3
方位0
方位1
方位10
方位11
方位12
方位2
方位3
方位4
方位5
方位6
方位7
方位8
方位9
时期0
时期1
时期2
检查实体0
检查实体1
检查实体10
检查实体11
检查实体12
检查实体13
检查实体2
检查实体3
检查实体4
检查实体5
检查实体6
检查实体7
检查实体8
检查实体9
检查方法0
检查方法1
检查方法2
检查方法3
检查方法4
气味0
活动度0
活动度1
程度0
程度1
程度2
程度3
程度4
程度5
等级0
等级1
等级2
等级3
等级4
等级5
等级6
等级7
等级8
等级9
结果性质0
结果性质1
结果性质2
结果性质3
节律0
节律1
范围大小0
范围大小1
范围大小2
范围大小3
范围大小4
范围大小5
范围大小6
质地0
质地1
质地2
趋势0
趋势1
趋势2
趋势3
身体部位0
身体部位1
身体部位10
身体部位11
身体部位12
身体部位13
身体部位14
身体部位2
身体部位3
身体部位4
身体部位5
身体部位6
身体部位7
身体部位8
身体部位9
限定条件0
限定条件1
限定条件2
限定条件3
限定条件4
音色音调0
音色音调1
音色音调2
频率和次数0
频率和次数1
频率和次数2
颜色0
颜色1
颜色2
颜色3""".split('\n')
    for r in deal_auto_set(s):
        print(r)
    # print(find_num('否定10'))
