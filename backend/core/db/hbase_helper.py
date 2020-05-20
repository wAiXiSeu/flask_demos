# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2019-12-02'
__description__ = doc description
"""

import happybase
import json


class HBaseHelper(object):
    def __init__(self, host="192.168.100.4", port=9090):
        self.host = host
        self.port = port
        self.connection = happybase.Connection(host=self.host, port=self.port, transport="framed")

    def get_table_data(self, table_name):
        table_data_generator = self.connection.table(table_name).scan(batch_size=100)
        for vid, info in table_data_generator:
            yield vid, self.load_case(info)

    def get_row_data(self, table_name, row):
        case = self.connection.table(table_name).row(row.encode("utf8"))
        return self.load_case(case)

    @staticmethod
    def load_case(row):
        case = {}
        for column, value in row.items():
            case[column.decode("utf8")] = json.loads(value)
        return case

