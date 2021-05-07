# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wAIxi'
__date__ = '2021/5/7'
__description__ = doc description
"""
import os
import sys

import pymysql
from DBUtils.PooledDB import PooledDB


class MySQLHelper:
    def __init__(self, host="localhost", port=3306, database="", user="root", password="", **kwargs):
        self.pool = PooledDB(pymysql, maxcached=10, maxconnections=50,
                             host=os.getenv("MYSQL_HOST", host),
                             port=int(os.getenv("MYSQL_PORT", port)),
                             database=os.getenv("MYSQL_DB", database),
                             user=os.getenv("MYSQL_USER", user),
                             password=os.getenv("MYSQL_PASSWORD", password),
                             **kwargs)

    def query(self, sql, ops="fetchall"):
        return self._execute(sql, ops=ops)

    def query_one(self, sql, ops="fetchone"):
        return self._execute(sql, ops=ops)

    def _execute(self, *args, **kwargs):
        conn = self.pool.connection()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        try:
            ops = kwargs.pop('ops') if 'ops' in kwargs else None
            r = cur.execute(*args, **kwargs)
            conn.commit()
            if ops is None:
                return r
            else:
                if hasattr(cur, ops):
                    r = getattr(cur, ops)()
                    return r
        except Exception as e:
            sys.stderr.write(str(e))
        finally:
            cur.close()
            conn.close()


mysql = MySQLHelper(port=13306, database='lishui_qc', user="root", password="123456")
