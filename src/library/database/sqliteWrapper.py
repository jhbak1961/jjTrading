# -*- coding: utf-8 -*-

"""
설명 : Oracle DB 연동을 위한 wrapper class
작성일 : 2017.
작성자 : smBak [TANGO-I/DR]
"""

import sqlite3
from operator import itemgetter

import library.log as log
from library.database.wrapper import DBWrapper


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


class SqliteWrapper(DBWrapper):
    def __init__(self, filename, auto_commit=None):
        DBWrapper.__init__(self)

        try:
            log.debug("Sqlite connection info. (%s)" % filename)
            # autoCommit : None | DEFERRED | IMMEDIATE | EXCLUSIVE
            self.connector = sqlite3.connect(filename, isolation_level=auto_commit)
            # self.connector = sqlite3.connect(filename)
        except:
            log.exception()
            raise

        try:
            self.cursor = self.connector.cursor()
        except:
            log.exception()
            raise

    def __iter__(self):
        return self.cursor.__iter__()

    def __getattr__(self, item):
        return getattr(self.cursor, item)

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

    def select(self, query, bind=None):
        try:
            if bind:
                self.cursor.execute(query, bind)
            else:
                self.cursor.execute(query)
        except:
            log.exception()
            raise

    def dml(self, query, bind=None):
        try:
            if bind:
                self.cursor.execute(query, bind)
            else:
                self.cursor.execute(query)
        except:
            raise

    def dmlMany(self, query, binds):
        try:
            self.cursor.executemany(query, binds)
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
