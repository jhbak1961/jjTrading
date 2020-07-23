# -*- coding: utf-8 -*-

"""
설명 : MySql DB 연동을 위한 wrapper class
작성일 : 2019.
작성자 : jihwan.Park
"""

import MySQLdb
from operator import itemgetter

import library.log as log
from library.database.wrapper import DBWrapper

version = "1.0.0"


class mysqlWrapper(DBWrapper):
    def __init__(self, user, passwd, dbname, host="localhost", port=3306, charset="utf8"):
        DBWrapper.__init__(self)

        try:
            log.debug(f"MySql connection info. ({host}:{user}/{passwd}@{dbname}")
            self.connector = MySQLdb.connect(host, user, passwd, dbname, port=port, charset=charset)
        except:
            log.exception()
            raise

        try:
            self.cursor = self.connector.cursor()
        except:
            log.exception()
            raise

    @property
    def rowcount(self):
        return self.cursor.rowcount

    def fetchcolumns(self):
        """SELECT 문 실행 후 column 리스트 리턴하는 method
            :return: list
        """
        if self.cursor.description is None:
            return []
        else:
            return [itemgetter(0)(metaT) for metaT in self.cursor.description]

    def fetchalldictlist(self):
        """SELECT 결과를 column:value 로 묶어서 [dict, dict, ....] 형태로 만들어서 전달하는 method.
            :return: list. [dict, dict, ...}
        """

        def __mergedata(row):
            return dict(zip(columns, row))

        columns = self.fetchcolumns()
        return map(__mergedata, self.cursor.fetchall())

    def iter_fetchalldict(self):
        """SELECT 결과를 column:value 로 묶어서 dict 값을 전달하는 반복자."""
        columns = self.fetchcolumns()
        for row in self.cursor.fetchall():
            yield dict(zip(columns, row))

    def select(self, statement, bind=None):
        """SELECT 문 실행을 위한 method

        :param statement: string. SQL 문장. (template 문자열, binding 변수 형식 모두 사용가능.)
        :param bind: tuple or list. binding 변수값.
        """
        try:
            if bind is None:
                self.cursor.execute(statement)
            else:
                self.cursor.execute(statement, bind)
        except:
            log.exception()
            raise

    def dml(self, statement, bind=None, autocommit=True):
        """INSERT, UPDATE, DELETE 문 실행을 위한 method

        :param statement: string. SQL 문장. (template 문자열, binding 변수 형식 모두 사용가능.)
        :param bind: tuple or list. binding 변수값.
        :param autocommit : boolean, auto commit. (default True)
        """
        return self._dml(statement, bind, autocommit)

    def dmlmany(self, statement, binds=None, autocommit=True):
        """INSERT, UPDATE, DELETE 문 실행을 위한 method

        :param statement: string. SQL 문장. (template 문자열, binding 변수 형식 모두 사용가능.)
        :param binds: double tuple or list. binding 변수값(tuple or list).
        :param autocommit : boolean, auto commit. (default True)
        """
        return self._dmlmany(statement, binds, autocommit)

    def insert(self, table, columns, bind, autocommit=True):
        """INSERT 실행을 위한 method

        :param table: 대상 Table 명
        :param columns: tuple or list. column 리스트.
        :param bind: tuple or list. binding 변수값. ex) binds=(var1, var2, var3)
        :param autocommit : boolean, auto commit. (default True)
        """
        if not isinstance(bind, tuple) and not isinstance(bind, list):
            raise TypeError("The variable(binds) should be type of a Tuple or List.")

        statement = self._make_insert_statement(table, columns, bind)
        # print(statement, bind)
        return self._dml(statement, bind, autocommit)

    def insertmany(self, table, columns, binds=None, autocommit=True):
        """INSERT 실행을 위한 method

        :param table: 대상 Table 명
        :param columns: tuple or list. column 리스트.
        :param binds: double tuple or list. binding 변수값. ex) binds=[(var1, var2, var3), ...]
        :param autocommit : boolean, auto commit. (default True)
        """
        if not isinstance(binds, tuple) and not isinstance(binds, list):
            raise TypeError("The variable(binds) should be type of a Tuple or List.")

        statement = self._make_insert_statement(table, columns, binds[0])
        # print(statement, binds)
        return self._dmlmany(statement, binds, autocommit)

    def delete(self, table, columns=None, bind=None, autocommit=True):
        """DELETE 실행을 위한 method

        :param table: 대상 Table 명
        :param columns: tuple or list. column 리스트.
        :param bind: tuple or list. binding 변수값. ex) bind=(var1, var2, var3)
        :param autocommit : boolean, auto commit. (default True)
        """
        if bind is not None and not isinstance(bind, tuple) and not isinstance(bind, list):
            raise TypeError("The variable(bind) should be type of a Tuple or List.")

        statement = self._make_delete_statement(table, columns)
        return self._dml(statement, bind, autocommit)

    def deletemany(self, table, columns=None, binds=None, autocommit=True):
        """DELETE 실행을 위한 method

        :param table: 대상 Table 명
        :param columns: tuple or list. column 리스트.
        :param binds: double tuple or list. binding 변수값. ex) binds=[(var1, var2, var3), ...]
        :param autocommit : boolean, auto commit. (default True)
        """
        if binds is not None and not isinstance(binds, tuple) and not isinstance(binds, list):
            raise TypeError("The variable(binds) should be type of a Tuple or List.")

        statement = self._make_delete_statement(table, columns)
        return self._dml(statement, binds, autocommit)

    def update(self, table, columns, before, after, autocommit=True):
        """UPDATE 실행을 위한 method

        :param table: 대상 Table 명
        :param columns: tuple or list. column 리스트
        :param before: tuple or list. 변경대상 값 리스트 ex) before=(var1, var2, var3)
        :param after: tuple or list. 변경 값 리스트 ex) after=(var11, var21, var31)
        :param autocommit : boolean, auto commit. (default True)
        """
        statement = self._make_update_statement(table, columns)
        bind = self._make_update_bind(columns, before, after)
        # update  처리된 레코드 수 를 반환한다.
        return self._dml(statement, bind, autocommit)

    def updatemany(self, table, columns, before, after, autocommit=True):
        """UPDATE 실행을 위한 method

        :param table: 대상 Table 명
        :param columns: tuple or list. column 리스트
        :param before: double tuple or list. 변경대상 값 리스트 ex) before=[(var1, var2, var3), ...]
        :param after: double tuple or list. 변경 값 리스트 ex) after=[(var11, var21, var31), ...]
        :param autocommit : boolean, auto commit. (default True)
        """
        statement = self._make_update_statement(table, columns)
        # before 와 after 를 Query 문에 맞게 재 배열하여 리스트로 만드는 부분
        # before=[(a,b,c),(e,f,g)] / after=[(1,2,3),(4,5,6)] ==> binds=[[1,2,3,a,b,c], [4,5,6,e,f,g]]
        binds = list()
        for row in range(len(before)):
            bind = self._make_update_bind(columns, before[row], after[row])
            binds.append(bind)

        # update  처리된 레코드 수 를 반환한다.
        return self._dmlmany(statement, binds, autocommit)


    def _dml(self, statement, bind=None, autocommit=True):
        try:
            self.cursor.execute(statement, bind)
            if autocommit:
                self.commit()

            return self.cursor.rowcount
        except:
            log.exception()
            if autocommit:
                self.rollback()
            raise

    def _dmlmany(self, statement, binds=None, autocommit=True):
        try:
            self.cursor.executemany(statement, binds)
            if autocommit:
                self.commit()

            return self.cursor.rowcount
        except:
            log.exception()
            if autocommit:
                self.rollback()
            raise

    def _make_insert_statement(self, table, columns, bind):
        if table is None:
            raise ValueError("No value set for 'table'.")
        if columns is not None and not isinstance(columns, tuple) and not isinstance(columns, list):
            raise TypeError("The variable(columns) should be type of a Tuple or List.")

        str_column = ""
        str_bind = ""
        if columns is None:
            # 컬럼정보 생략된 형태의 insert 문장. (SQL = INSERT INTO 테이블명 VALUES (%s, %s, ...))
            if bind is not None:
                for idx, col in enumerate(bind):
                    if idx != 0:
                        str_bind += ","
                    str_bind += "%s"
        else:
            # 컬럼정보 생략된 형태의 insert 문장. (SQL = INSERT INTO 테이블명 (컬럼1, 컬럼2,..) VALUES (%s, %s,...))
            for idx, col in enumerate(columns):
                if idx != 0:
                    str_column += ","
                    str_bind += ","
                str_column += col
                str_bind += "%s"

        str_column = " (%s) " % str_column if str_column else ""
        statement = "INSERT INTO %s %s VALUES(%s)" % (table, str_column, str_bind)
        return statement

    def _make_delete_statement(self, table, columns):
        if table is None:
            raise ValueError("No value set for 'table'.")
        if columns is not None and not isinstance(columns, tuple) and not isinstance(columns, list):
            raise TypeError("The variable(columns) should be type of a Tuple or List.")

        str_where = ""
        if columns:
            for idx, col in enumerate(columns):
                str_where += " WHERE " if idx == 0 else " AND "
                str_where += col + "=" + "%s"

        return "DELETE FROM %s %s" % (table, str_where)

    def _make_update_statement(self, table, columns):
        if table is None:
            raise ValueError("No value set for 'table'.")
        if not isinstance(columns, tuple) and not isinstance(columns, list):
            raise TypeError("The variable(columns) should be type of a Tuple or List.")

        # Column 을 기준으로 SET, WHERE 문장을 만들어 내는 부분.
        # columns(a,b,c) 인 경우 : SET문장==> a=%s, b=%s, c=%s / WHERE문장 ==> a=%s and b=%s and c=%s
        str_set = ""
        str_where = ""
        for idx, col in enumerate(columns):
            if idx != 0:
                str_set += ", "
                str_where += " and "
            str_set += col + "=" + "%s"
            str_where += col + "=" + "%s"

        return "UPDATE %s SET %s WHERE %s" % (table, str_set, str_where)

    def _make_update_bind(self, columns, before, after):
        if not isinstance(before, tuple) and not isinstance(before, list):
            raise TypeError("The variable(before) should be type of a Tuple or List.")

        if not isinstance(after, tuple) and not isinstance(after, list):
            raise TypeError("The variable(after) should be type of a Tuple or List.")

        # before 와 after 를 Query 문에 맞게 재 배열하여 리스트로 만드는 부분
        # before=(a,b,c) / after=(1,2,3) ==> binds=[1,2,3,a,b,c]
        bind = list()
        for idx in range(len(columns)):
            bind.append(after[idx])
        for idx in range(len(columns)):
            bind.append(before[idx])

        return bind
