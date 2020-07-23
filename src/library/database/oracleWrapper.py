# -*- coding: utf-8 -*-

""" 
설명 : Oracle DB 연동을 위한 wrapper class
작성일 : 2017.
작성자 : smBak [TANGO-I/DR]
"""

from operator import itemgetter

import cx_Oracle

from common import log
from common import utility
from common.db.wrapper import DBWrapper

version = "1.0.0"


def filterBindKeysDict(keys, bind):
    """
    dict 에서 query 문의 bind 변수에 해당하는 값만 추출하여 결과로 전달 하는 함수

    :param keys: list. binding 변수 key값 리스트
    :param bind: dict. binding 변수에 해당하는 값이 포함된 dictionary
    :return: bindig 변수와 값을 조합한 dict.
    """

    rtnData = dict((k, bind.get(k)) for k in keys)
    return rtnData


def filterBindKeysList(keys, bind):
    """
    list 에서 query 문의 bind 변수에 해당하는 값만 추출하여 결과로 전달 하는 함수

    :param keys: list. binding 변수 index 값 리스트
    :param bind: list. binding 변수에 해당하는 값이 포함된 list
    :return: bindig 변수와 값을 조합한 dict.
    """

    rtnData = dict((k, bind[int(k)]) for k in keys)
    return rtnData


class OracleWrapper(DBWrapper):
    def __init__(self, userId, passwd, sid, encoding="utf-8", nencoding="utf-8"):
        DBWrapper.__init__(self)

        try:
            log.debug("Oracle connection info. (%s/%s@%s)" % (userId, passwd, sid))
            self.connector = cx_Oracle.connect(userId, passwd, sid, encoding=encoding, nencoding=nencoding)
        except:
            log.exception()
            raise

        try:
            self.cursor = self.connector.cursor()
        except:
            log.exception()
            raise

    # def __iter__(self):
    #     return self.cursor.__iter__()
    #
    # def __getattr__(self, item):
    #     return getattr(self.cursor, item)

    @property
    def rowcount(self):
        return self.cursor.rowcount

    def _filterDataBindKeys(self, bind):
        if isinstance(bind, dict):
            vD = filterBindKeysDict(self.cursor.bindnames(), bind)
        elif isinstance(bind, list):
            vD = filterBindKeysList(self.cursor.bindnames(), bind)
        elif isinstance(bind, tuple):
            vD = filterBindKeysList(self.cursor.bindnames(), bind)
        else:
            vD = None
        return vD

    def prepare(self, query):
        if self.cursor.statement != query:
            self.cursor.prepare(query)

    def execute(self, query, bind=None):
        """SQL 문장 실행을 위한 method.

        :param query: string. SQL 문장. (template 문자열, binding 변수 형식 모두 사용가능.)
        :param bind: dict. binding 변수값.
        """

        if bind is None:
            self.cursor.execute(query)
        else:
            # 테이블명은 bind 변수 처리가 불가해서, Template 문자열 처리 방식을 이용하도록 한다.
            statement = utility.expandString(query, bind)
            statement = statement.format(bind)
            self.prepare(statement)

            vBind = self._filterDataBindKeys(bind)
            self.cursor.execute(None, vBind)

    def executeMany(self, query, bindDataList, maxBachRows=5000):
        """
        다수의 데이터 리스트를 처리하기 위한 method

        :param query: string. SQL 문
        :param bindDataList: list. binding 데이터 리스트
        :param maxBachRows: int. 한번에 처리할 최대 row 개수
        """
        self.prepare(query)
        inBindList = map(self._filterDataBindKeys, bindDataList)

        try:
            self.cursor.executemany(None, inBindList)
        except:
            raise

    def fetchColumns(self):
        """
        SELECT 문 실행 후 column 리스트 리턴하는 method
        :return: list
        """
        if self.cursor.description is None:
            return []
        else:
            return [itemgetter(0)(metaT) for metaT in self.cursor.description]

    def fetchAllDictList(self):
        """
        SELECT 결과를 column:value 로 묶어서 [dict, dict, ....] 형태로 만들어서 전달하는 method.
        :return: list. [dict, dict, ...}
        """

        def __mergedata(row):
            return dict(zip(columns, row))

        columns = self.fetchColumns()
        return map(__mergedata, self.cursor.fetchall())

    def fetchAllDictIter(self):
        """
        SELECT 결과를 column:value 로 묶어서 dict 값을 전달하는 반복자.

        """
        columns = self.fetchColumns()
        for row in self.cursor.fetchall():
            yield dict(zip(columns, row))

    def commit(self):
        self.connector.commit()

    def rollback(self):
        self.connector.rollback()
