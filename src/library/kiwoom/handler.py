# -*- coding: utf-8 -*-

# Description : 
# Date : 
# Author : Jayden.Park (jhpark)
import sys

from PyQt5.QAxContainer import QAxWidget
from datetime import datetime as dt

from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication


class JJKiwoom(QAxWidget):
    __instance = None

    @classmethod
    def __get_instance(cls):
        # print(f"__get()")
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kwargs):
        # print("instance()")
        cls.__instance = cls(*args, **kwargs)
        # instance() 를 __get_instance() 함수로 대체시킴
        cls.instance = cls.__get_instance
        return cls.__instance

    def __init__(self, controlName):
        super().__init__()
        self.setControl(controlName)

        self.connectState = False

        self.loginLoop = None

        # Event 처리
        self.OnEventConnect.connect(self.eventConnect)
        # self.OnReceiveTrData.connect(self.eventReceiveTrData)
        # self.OnReceiveChejanData.connect(self.eventReceiveChejanData)
        # self.OnReceiveMsg.connect(self.eventReceiveMsg)

    def eventConnect(self, returnCode):
        """ 통신 연결 상태 변경시 이벤트
        returnCode가 0이면 로그인 성공
        그 외에는 ReturnCode 클래스 참조.

        Parameters
        ----------
        returnCode: int
            0이면 로그인 성공, 이외에는 로그인 실패
        """
        print(f"evetnConnect(): {returnCode}")
        if returnCode == 0:
            self.connectState = True
            msg = f"{dt.now()} Connection Successful"
        else:
            # errorName = getattr(ReturnCode, "CAUSE").get(returnCode)
            # msg = "{} Connection Failed : {}".format(dt.now(), errorName)
            msg = f"{dt.now()} Connection Failed : {returnCode}"

        print(msg)
        # self.logger.debug(msg)

        try:
            self.loginLoop.exit()
        except AttributeError:
            pass

    def commConnect(self):
        """ 로그인 시도 """

        if not self.connectState:
            self.dynamicCall("CommConnect()")
            self.loginLoop = QEventLoop()
            self.loginLoop.exec_()  # eventConnect에서 loop를 종료



if __name__ == '__main__' :
    app = QApplication(sys.argv)

    jo = JJKiwoom("KHOPENAPI.KHOpenAPICtrl.1")
    jo.commConnect()