# -*- coding: utf-8 -*-
"""
설명 : DB Wrapper 의 기본 구조 정의 class
작성일 : 2017.
작성자 : smBak [TANGO-I/DR]
"""

import library.log as LOG

class DBWrapper(object):
    def __init__(self):
        self.__connector = None
        self.__cursor = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __iter__(self):
        return self.__cursor.__iter__()

    def __getattr__(self, item):
        return getattr(self.__cursor, item)

    def __del__(self):
        LOG.debug()
        self.close()

    @property
    def connector(self):
        return self.__connector

    @connector.setter
    def connector(self, new_connector):
        self.__connector = new_connector

    @property
    def cursor(self):
        return self.__cursor

    @cursor.setter
    def cursor(self, new_cursor):
        self.__cursor = new_cursor

    def close(self):
        if self.__cursor is not None:
            self.__cursor.close()
            self.__cursor = None

        if self.__connector is not None:
            self.__connector.close()
            self.__connector = None

    # @abc.abstractmethod
    # def execute(self, *args, **kwargs):
    #     pass
    #
    # @abc.abstractmethod
    # def executeMany(self, *args, **kwargs):
    #     pass


    def commit(self):
        self.__connector.commit()

    def rollback(self):
        self.__connector.rollback()