# -*- coding: utf-8 -*-

import os
import pathlib
import sys
from matplotlib import font_manager, rc
from optparse import OptionParser

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

# import library.log as LOG
from view.controller.ctrl_main_view import Ctrl_MainWindow
# from library.database import mysqlWrapper


# def main(config_dict, font_file, icon_file):
def main(config_dict):
    # 한글 폰트 설정
    # font_file = os.path.normpath(os.path.expandvars("${PJT_HOME}/resource/fonts/malgun.ttf"))
    # font_name = font_manager.FontProperties(fname=font_file).get_name()
    # rc("font", family=font_name, size=8)
    # LOG.debug(font_name)

    # db_obj = mysqlWrapper.mysqlWrapper(config_dict["DataBase"]["USER"],
    #                                    config_dict["DataBase"]["PASSWD"],
    #                                    config_dict["DataBase"]["NAME"],
    #                                    config_dict["DataBase"]["HOST"]
    #                                    )

    # Main ui_design open
    app = QtWidgets.QApplication(sys.argv)
    main_window = Ctrl_MainWindow()
    # main_window = Ctrl_MainWindow(db_obj=db_obj)
    # main_window.setWindowIcon(QIcon(icon_file))
    # main_window.setWindowTitle("더 강사")
    # main_window.showMaximized()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # 현재 디렉터리의 상위 디렉터리를 BIZ_HOME 으로 설정
    # if "BIZ_HOME" not in os.environ:
    #     os.environ["PJT_HOME"] = str(pathlib.Path(os.getcwd()).parent)

    # usage = """usage: %prog [options] config_file(file name)
    #     ex) -eDEV
    #     """
    # argParser = OptionParser(usage=usage)
    # argParser.add_option("-e", "--execut_mode", dest="exe_mode", default="DEV",
    #                      help="process excute mode. (DEV/EXE)")
    # argParser.add_option("-l", "--log_level", dest="log_level", default="DEBUG",
    #                      help="logging level. (default=INFO)")
    #
    # (options, args) = argParser.parse_args()
    #
    # if options.exe_mode.upper() not in ("DEV", "EXE"):
    #     argParser.print_help()
    #     sys.exit()
    #
    # if len(args) != 1:
    #     argParser.print_help()
    #     sys.exit()
    #
    # import json
    #
    # print(">", os.getcwd())
    #
    # if not os.path.exists(os.path.normpath(args[0])):
    #     print("config file is not exists. (%s)" % os.path.normpath(args[0]))
    #     sys.exit()
    #
    # with open(args[0], 'r') as f:
    #     dict_config = json.load(f)
    #
    # if options.exe_mode.upper() == "DEV":
    #     os.environ["PJT_HOME"] = str(pathlib.Path(os.getcwd()).parent)
    # else :
    #     os.environ["PJT_HOME"] = str(pathlib.Path(os.getcwd()))
    #
    # print("PJT_HOME >", os.environ["PJT_HOME"])
    #
    # #     font_file_name = os.path.normpath(os.path.expandvars(os.path.join(os.getcwd(), "resource", "fonts", "malgun.ttf")))
    # #     icon_file_name = os.path.normpath(os.path.expandvars(os.path.join(os.getcwd(), "resource", "icon", "logo.png")))
    # # else:
    # #     font_file_name = os.path.normpath(os.path.expandvars(os.path.join(os.getcwd(), "resource", "fonts", "malgun.ttf")))
    # #     icon_file_name = os.path.normpath(os.path.expandvars(os.path.join(os.getcwd(), "resource", "icon", "logo.png")))
    #
    # if options.log_level is not None:
    #     LOG.InitBaseLog(options.log_level)
    # else :
    #     LOG.InitBaseLog(LOG.DEBUG)
    #
    # main(dict_config)

    main({})
