# -*- coding: utf-8 -*-
"""
설명 : 공통으로 사용되는 기능을 함수 형태로 만들어 제공
작성일 : 2019.10
작성자 : Jayden.Park
"""

import datetime
import json
import string


def serializeToJSON(python_object):
    """python object 중에서 JSON 문자열로 기본 변환이 안되는 데이터에 대한 변환 기능 제공

    :param python_object : object. JSON 문자열로 바꾸기 위한 object
    :return : string. 변경된 JSON 문자열.

    >>> nowdate = datetime.datetime.now()
    >>> json.dumps(nowdate, default=serializeToJSON)
    >>> {'__class__':'datetime', '__value__' : 'datetime.datetime(2017, 5, 30, 17, 52, 16, 295000)'}

    """

    if isinstance(python_object, datetime.datetime):
        return {"__class__": "datetime",
                "__value__": repr(python_object)
                }
    else:
        raise TypeError(repr(python_object)+"is not JSON serializable")


def deserializeFromJSON(json_object):
    """JSON 문자열의 내용중 기본 object 변환이 안되는 데이터에 대하여 변환 기능 제공

    :param json_object : string. json 형식의 문자열
    :return : object. 변환된 object 반환
    """
    if json_object.get("__class__", "") == "datetime":
        return eval(json_object.get("__value__"))
    else:
        return json_object


def codec2codec(val, decodec, encodec):
    """한글 encoding 변환"""
    if isinstance(val, str):
        try:
            dVal = val.decode(decodec, "ignore").encode(encodec)
        except:
            return ""
        else:
            return dVal
    else:
        return val


def uencode(val, decodec="utf-8", encodec="utf-8"):
    if isinstance(val, str):
        return val.decode(decodec, "ignore").encode(encodec)
    else:
        return val


def expandString(templateString, bindD):
    """ 템플릿 형태의 문자열의 바인딩변수의 값을 매칭하여 문자열을 만들어 준다.

    :param str templateString: 템플릿 문자열
    :param dic bindD : 템플릿 문자열에 바인딩할 데이터
    :returns : 문자열

    >>> print expandString('${bind1}${bind2}', {'bind1':'123', 'bind2':'abc'})
    """

    t = string.Template(templateString)
    return t.safe_substitute(bindD)


def dec2bin(num, bitsize=8):
    """
    숫자를 bit string으로 변환하여 전달한다. 10 -> 00001010
    :param num: 변환할 숫자
    :param bitsize: bit string의 자리수
    :return: bit string.
    """
    if not isinstance(num, int):
        return None
    bStrFormat = "{:0%db}" % bitsize
    return bStrFormat.format(num)  # bitsize 크기의 bit 문자열로 변환 A->1010
