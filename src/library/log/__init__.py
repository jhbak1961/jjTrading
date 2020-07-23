# -*- coding: utf-8 -*-

"""
Description :프로그램 상에서 필요에 의해 현재 처리상태, 데이터 등의 값을 text로 표시할때 사용.
            : 파일형태, console out 형태등 선택해서 표시 할 수 있다.
date        : 2017.
creator     : Jayden.Park
"""


import logging
import logging.handlers
import operator
import os
from functools import wraps
from traceback import extract_stack

version = "1.0.4"

DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

# DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
DATE_FORMAT = None
# LOG_TEMPLATE = "[%(asctime)s][%(levelname)-7s:%(threadName)s:%(name)s]:%(message)s"
LOG_TEMPLATE = "[%(asctime)s][%(levelname)-7s]:%(message)s"
MSG_TEMPLATE = "%(pid)5d>%(fileName)s-%(methodName)s(%(lineNumber)3d) : %(text)s"


def deco_method(func):
    """log 출력 하는 DATA 를 일정 형식으로 만들기 위한 decorator 함수.
        문자열은 기본 출력 하지만, 그외 type은 특정 형태로 표현 한다.
        예) dict type 인 경우
        #
        # type : (type : dict)
        # key1 : value1
        # key2 : value2
        #
    """
    @wraps(func)
    def wrapper(*args):
        tL = []
        # print 'args>>>', args, func
        nowLogger = None
        for val in args:
            if isinstance(val, logging.Logger):
                nowLogger = val
            elif isinstance(val, dict):
                if len(tL) == 0: tL.append("")  # log 메시지 없이 object 의 값을 출력시 line 분리를 위한 용도.
                tL.append("#")
                tL.append("# value is %s" % (type(val)))
                for k, v in sorted(val.items(), key=operator.itemgetter(0)):
                    tL.append("# %15s : %-50s %10s" % (k, v, type(v)))

                tL.append("#")
            elif isinstance(val, list) or isinstance(val, tuple):
                if len(tL) == 0: tL.append("")  # log 메시지 없이 object 의 값을 출력시 line 분리를 위한 용도.
                tL.append("#")
                tL.append("# value is %s" % (type(val)))
                for k, v in enumerate(val):
                    tL.append("# %-15d : %-50s %10s" % (k, v, type(v)))

                tL.append("#")
            else:
                if len(tL) == 0 and isinstance(val, str) :
                    tL.append(val)
                elif len(tL) > 0:
                    tL.append("# %-50s %10s" % (val, type(val)))
                else:
                    tL.append("")
                    tL.append("# %-50s %10s" % (val, type(val)))

        # 함수 호출 stack 리스트중 log 함수 호출한 부분부터의 리스트 만 가져오는 부분
        stackL = extract_stack()[-2:][0]

        # log 출력 포멧에 맞춰서 메시지 생성하는 부분
        paramD = dict()
        paramD["fileName"] = os.path.basename(stackL[0])
        paramD["lineNumber"] = stackL[1]
        paramD["methodName"] = stackL[2]
        paramD["text"] = "\n".join(tL)
        paramD["pid"] = os.getpid()

        func(nowLogger, MSG_TEMPLATE % paramD)


    return wrapper


def InitBaseLog(logLevel=logging.INFO, newRoot=True):
    """기본 stderr로 출력 하는 logger

    :param logLevel : const string. 로그 남기는 최소 레벨. (debug<info<warning<error<critical)
    :param newRoot : boolean. 신규 root logger 설정. (default is True)
    """

    handler = getStreamHandler()

    rootLogger = logging.getLogger()
    rootLogger.setLevel(logLevel)
    if newRoot:
        while rootLogger.handlers:
            # debug('logger old handler delete. >', rootLogger.name, rootLogger.handlers)
            rootLogger.removeHandler(rootLogger.handlers.pop())
        rootLogger.addHandler(handler)

    return rootLogger


def InitTimeRotatingLog(logFile, when="MIDNIGHT", logLevel=logging.INFO,
                        interval=1, backupCnt=7, delay=False, newRoot=True):
    """시간별 로그 파일 생성하는 logger

     :param logFile: string. 로그 파일 full path
     :param when : const string. 로그파일 변경 시점 단위. (H:hour,D/MIDNIGHT:daily)
     :param logLevel : const string. 로그 남기는 최소 레벨. (debug<info<warning<error<critical)
     :param interval : int.  로그파일 변경 간격.
     :param backupCnt : int. 로그파일 최대 저장 개수
     :param delay : 파일의 rollover 시점을 첫 로그 작성이후로 delay 시킴 여부
     :param newRoot : boolean. 신규 root logger 설정. (default is True)
    """

    handler = getTimeRotaingHandler(logFile, when, interval, backupCnt, delay)

    rootLogger = logging.getLogger()
    rootLogger.setLevel(logLevel)
    if newRoot:
        while rootLogger.handlers:
            # debug('logger old handler delete. >', rootLogger.name, rootLogger.handlers)
            rootLogger.removeHandler(rootLogger.handlers.pop())
        rootLogger.addHandler(handler)

    return rootLogger


KB = 1024
MB = 1024 * 1024
GB = 1024 * 1024 * 1024


def InitRotatingLog(logfile, maxSize=5 * MB, backCnt=5, logLevel=logging.INFO, delay=False, newRoot=True):
    """logging의 root Handler의 기본 설정 class

    :param logfile: string. 로그 파일 full path
    :param maxSize : int. 파일의 최대 크기. (기본 5Mbyte [KB, MB, GB])
    :param backCnt : int. 파일을 생성 개수. (설정값 이상으로 파일 생성될 시 첫번째 파일부터 삭제후 재생성)
    :param logLevel : const string. 로그 남기는 최소 레벨. (debug<info<warning<error<critical)
    :param delay : 파일의 rollover 시점을 첫 로그 작성이후로 delay 시킴 여부
    :param newRoot : boolean. 신규 root logger 설정. (default is True)
    """

    handler = getRotaingHandler(logfile, maxSize, backCnt, delay)

    rootLogger = logging.getLogger()
    rootLogger.setLevel(logLevel)
    if newRoot:
        while rootLogger.handlers:
            # debug('logger old handler delete. >', rootLogger.name, rootLogger.handlers)
            rootLogger.removeHandler(rootLogger.handlers.pop())
        rootLogger.addHandler(handler)

    return rootLogger


def getStreamHandler():
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(logging.Formatter(LOG_TEMPLATE, DATE_FORMAT))
    return hdlr


def getTimeRotaingHandler(fileName, when="MIDNIGHT", interval=1, backupCnt=7, delay=False):
    hdlr = logging.handlers.TimedRotatingFileHandler(fileName, when, interval, backupCnt, delay=delay)
    hdlr.setFormatter(logging.Formatter(LOG_TEMPLATE, DATE_FORMAT))
    return hdlr


def getRotaingHandler(fileName, maxSize=5 * MB, backCnt=5, delay=False):
    hdlr = logging.handlers.RotatingFileHandler(fileName, maxBytes=maxSize, backupCount=backCnt, delay=delay)
    hdlr.setFormatter(logging.Formatter(LOG_TEMPLATE, DATE_FORMAT))
    return hdlr


def getLogger(name=None):
    return logging.getLogger(name)


@deco_method
def info(*args):
    if isinstance(args[0], logging.Logger):
        args[0].info(*args[1:])
    else:
        logging.info(*args[1:])


@deco_method
def debug(*args):
    if isinstance(args[0], logging.Logger):
        args[0].debug(*args[1:])
    else:
        logging.debug(*args[1:])


@deco_method
def warning(*args):
    if isinstance(args[0], logging.Logger):
        args[0].warning(*args[1:])
    else:
        logging.warning(*args[1:])


@deco_method
def warn(*args):
    if isinstance(args[0], logging.Logger):
        args[0].warning(*args[1:])
    else:
        logging.warning(*args[1:])


@deco_method
def error(*args):
    if isinstance(args[0], logging.Logger):
        args[0].error(*args[1:])
    else:
        logging.error(*args[1:])


@deco_method
def exception(*args):
    if isinstance(args[0], logging.Logger):
        args[0].exception(*args[1:])
    else:
        logging.exception(*args[1:])



#
# class SMLogger(object):
#     def __init__(self, name=None, logLevel=DEBUG, handler=None):
#         if name is None:
#             # root = logging.RootLogger(logLevel)
#             # logging.Logger.root = root
#             # logging.Logger.manager = logging.Manager(logging.Logger.root)
#             # self._logger = logging.Logger.manager.getLogger(name)
#             self._logger = logging.RootLogger(logLevel)
#             logging.root = self._logger
#         else:
#             self._logger = logging.getLogger(name)
#             self._logger.setLevel(logLevel)
#
#         if handler:
#             if self._logger.handlers:
#                 while self._logger.handlers:
#                     self._logger.removeHandler(self._logger.handlers.pop())
#                 self.addHandler(handler)
#
#
#     def decoclassmethod(func):
#         @wraps(func)
#         def wrapper(self, *args):
#             tL = []
#             # print 'wrapper >>>', args, func.__name__
#             for val in args:
#                 if isinstance(val, dict):
#                     if len(tL) == 0: tL.append("")  # log 메시지 없이 object 의 값을 출력시 line 분리를 위한 용도.
#                     tL.append("#")
#                     tL.append("# value is %s" % (type(val)))
#                     for k, v in val.items():
#                         tL.append("# %s : %s \t%s" % (utility.uni2str(k), utility.uni2str(v), type(v)))
#
#                     tL.append("#")
#                 elif isinstance(val, list) or isinstance(val, tuple):
#                     if len(tL) == 0: tL.append("")  # log 메시지 없이 object 의 값을 출력시 line 분리를 위한 용도.
#                     tL.append("#")
#                     tL.append("# value is %s" % (type(val)))
#                     for k, v in enumerate(val):
#                         tL.append("# %d : %s \t%s" % (k, utility.uni2str(v), type(v)))
#
#                     tL.append("#")
#                 else:
#                     if len(tL) == 0 and isinstance(val, str):
#                         tL.append(val)
#                     elif len(tL) > 0:
#                         tL.append("# %s %s" % (val, type(val)))
#                     else:
#                         tL.append("%s %s" % (val, type(val)))
#
#             # 함수 호출 stack 리스트중 log 함수 호출한 부분부터의 리스트 만 가져오는 부분
#             stackL = extract_stack()[-2:][0]
#
#             # log 출력 포멧에 맞춰서 메시지 생성하는 부분
#             paramD = {}
#             paramD["fileName"] = os.path.basename(stackL[0])
#             paramD["lineNumber"] = stackL[1]
#             paramD["methodName"] = stackL[2]
#
#             # return func("\n".join(tL))
#             paramD["text"] = "\n".join(tL)
#
#             # print self, self._logger, func.__name__
#             func(self, MSG_TEMPLATE % paramD)
#
#
#         return wrapper
#
#
#     def addHandler(self, handler=None):
#         if handler is None:
#             handler = getStreamHandler()
#
#         self._logger.addHandler(handler)
#         # print len(self._logger.handlers)
#
#
#     @decoclassmethod
#     def info(self, *args):
#         self._logger.info(*args)
#
#
#     @decoclassmethod
#     def debug(self, *args):
#         self._logger.debug(*args)
#         # print "debug>>>>", args
#         # print len(self._logger.handlers)
#
#
#     @decoclassmethod
#     def warning(self, *args):
#         self._logger.warning(*args)
#
#
#     @decoclassmethod
#     def error(self, *args):
#         self._logger.error(*args)
#
#
#     @decoclassmethod
#     def exception(self, *args):
#         self._logger.exception(*args)
#
