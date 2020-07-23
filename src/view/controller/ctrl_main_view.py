# -*- coding: utf-8 -*-
import sys

from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QCoreApplication, pyqtSlot, Qt

# from controller.crtl_dlg_input_csat import Ctrl_DialogInputCSAT
# from controller.crtl_dlg_input_hss import Ctrl_DialogInputHSS
# from controller.crtl_dlg_input_student import Ctrl_DialogInputStudent
# from controller.crtl_dlg_login import Ctrl_DiglogLogin
from PyQt5.QtWidgets import QMessageBox

from view.form.mw_main import Ui_MainWindow
import library.log as LOG


class Ctrl_MainWindow(Ui_MainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags(), db_obj=None):
        super().__init__(parent=parent, flags=flags, db_obj=db_obj)
        self._kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        # login 화면 표시
        # self._check_login()

        # Menu Action 기능정의
        # self.actionAddStudent.triggered.connect(self.slot_open_input_student)
        # self.actionManageStudent.triggered.connect(self.slot_open_manage_student)
        # self.actionExit.triggered.connect(QCoreApplication.quit)
        #
        # self.actionAdd_CSAT_Score.triggered.connect(self.slot_open_input_csat)
        # self.actionAdd_HSS_Score.triggered.connect(self.slot_open_input_hss)
        #
        # self.actionAddEarlyDecision.triggered.connect(self.slot_open_early_decision)
        # self.actionEarlyPassPresent.triggered.connect(self.slot_open_early_passpresent)
        # self.actionAddRegularDecision.triggered.connect(self.slot_open_regular_decision)
        # self.actionRegularPassPresent.triggered.connect(self.slot_open_regular_passpresent)

        # slot & connect
        # self.btnSearch.clicked.connect(self.slot_search_present)
        # self.btnOpenDlgStudent.clicked.connect(self.slot_open_dlg_student)
        # self.btnOpenDlgEntrace.clicked.connect(self.slot_open_dlg_entrace)
        self.pushButton.clicked.connect(self._slot_login)
        self.pushButton_2.clicked.connect(self._slot_get_status)
        self.pushButton_3.clicked.connect(self._slot_get_baseinfo)

        # OPEN API+ Event 설정
        # 통신 연결 상태 변경시 이벤트
        self._kiwoom.OnEventConnect.connect(self._event_connect)
        self._kiwoom.OnReceiveTrData.connect(self._event_receive_trdata)

    @property
    def ocx_kiwoom(self):
        return self._kiwoom

    def _event_connect(self, err_code):
        if err_code == 0:
            self.statusBar().showMessage("로그인 성공")
        else:
            self.statusBar().showMessage(f"ConnectEvent > ErrorCode : {err_code}")
            # QMessageBox.warning(None, "확인요청", f"ErrorCode : {err_code}", QMessageBox.Ok)

    def _event_receive_trdata(self, scr_no, rq_name, tr_code, record_nm, prev_next, data_len, err_cd, msg1, spl_msg):
        if rq_name == "opt10001_req" :
            self._recv_opt10001(scr_no, rq_name, tr_code, record_nm, prev_next)


    def _recv_opt10001(self, scr_no, rq_name, tr_code, record_nm, prev_next):
        self.statusBar().showMessage(f"{scr_no, rq_name, tr_code, record_nm, prev_next}")
        ncnt = self._kiwoom.dynamicCall("GetDataCount(QString)", "주식기본정보")
        self.statusBar().showMessage(f"record count:{ncnt}")
        name = self._kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, "주식기본정보", 0, "종목명")
        volume = self._kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, "주식기본정보", 0, "거래량")
        # self.statusBar().showMessage(f"{name.strip()}")
        # self.statusBar().showMessage(f"{volume.strip()}")

        self.textEdit.append("종목명: " + name.strip())
        self.textEdit.append("거래량: " + volume.strip())


    @pyqtSlot()
    def _slot_login(self):
        self._kiwoom.dynamicCall("CommConnect()")

    @pyqtSlot()
    def _slot_get_status(self):
        if self._kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")


    @pyqtSlot()
    def _slot_get_baseinfo(self):
        code = self.lineEdit.text()
        self.textEdit.append("종목코드: " + code)

        # SetInputValue
        self._kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)

        # CommRqData
        self._kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")

    # def _check_login(self):
    #     dlg_login = Ctrl_DiglogLogin(db_obj=self._dbobj)
    #     dlg_login.show()
    #     dlg_login.exec_()
    #
    #     LOG.debug("login result > ", dlg_login.islogin)
    #     if not dlg_login.islogin:
    #         sys.exit()
    #
    # @pyqtSlot()
    # def slot_open_input_student(self):
    #     # 신규 입력창을 만들어서 표시하는 방법으로 실행
    #     dlgRegist = Ctrl_DialogInputStudent(self, db_obj=self._dbobj)
    #     dlgRegist.show()
    #     dlgRegist.exec_()
    #     # insert 후 list에 반영되도록 화면 처리
    #     LOG.debug("Regist student dialog : ", dlgRegist.changed)
    #     if dlgRegist.changed:
    #         wd = self.stackedWidget.widget(0)
    #         LOG.debug(wd, self.stackedWidget.currentIndex(), self.stackedWidget.currentWidget())
    #         if self.stackedWidget.currentIndex() == 0:
    #             wd.refresh_student_list()
    #
    # @pyqtSlot()
    # def slot_open_input_csat(self):
    #     # 신규 입력창을 만들어서 표시하는 방법으로 실행
    #     dlgRegist = Ctrl_DialogInputCSAT(self, db_obj=self._dbobj)
    #     dlgRegist.show()
    #     dlgRegist.exec_()
    #
    # @pyqtSlot()
    # def slot_open_input_hss(self):
    #     # 신규 입력창을 만들어서 표시하는 방법으로 실행
    #     dlgRegist = Ctrl_DialogInputHSS(self, db_obj=self._dbobj)
    #     dlgRegist.show()
    #     dlgRegist.exec_()
    #
    # @pyqtSlot()
    # def slot_open_manage_student(self):
    #     self.stackedWidget.setCurrentIndex(0)
    #
    # @pyqtSlot()
    # def slot_open_early_decision(self):
    #     self.stackedWidget.setCurrentIndex(1)
    #
    # @pyqtSlot()
    # def slot_open_early_passpresent(self):
    #     self.stackedWidget.setCurrentIndex(2)
    #
    # @pyqtSlot()
    # def slot_open_regular_decision(self):
    #     self.stackedWidget.setCurrentIndex(3)
    #
    # @pyqtSlot()
    # def slot_open_regular_passpresent(self):
    #     self.stackedWidget.setCurrentIndex(4)
